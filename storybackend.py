# #...new code
# from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# from fastapi.concurrency import run_in_threadpool
# from fastapi.responses import FileResponse
# from pydantic import BaseModel
# import os
# import time
# import json
# import traceback
# import threading
# from typing import List, Dict, Optional
# import logging
# import sys


# # For AI and Cloud services
# from google.genai import Client
# from google.genai.types import GenerateVideosConfig
# from google.cloud import texttospeech
# from google.cloud import translate_v2 as translate
# from dotenv import load_dotenv

# # For Spelling Correction
# from spellchecker import SpellChecker


# load_dotenv()

# # ======================================================================================
# # LOGGING CONFIGURATION
# # ======================================================================================
# log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
# logger = logging.getLogger()
# logger.setLevel(logging.INFO) 

# # --- FileHandler block is commented out as requested ---
# # try:
# #     file_handler = logging.FileHandler("app.log", encoding='utf-8')
# #     file_handler.setFormatter(log_formatter)
# #     logger.addHandler(file_handler)
# # except Exception as e:
# #     print(f"Failed to create file logger: {e}")
# # --- END OF CHANGE ---

# try:
#     stream_handler = logging.StreamHandler(sys.stdout)
#     stream_handler.setFormatter(log_formatter)
#     if sys.version_info >= (3, 10):
#         stream_handler.setEncoding('utf-8')
#     logger.addHandler(stream_handler)
# except Exception as e:
#     print(f"Failed to create stream logger: {e}")
#     if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
#         try:
#             logger.addHandler(logging.StreamHandler(sys.stdout))
#             logger.warning("StreamHandler UTF-8 encoding failed (likely < Python 3.10). Emojis may not display correctly in console.")
#         except Exception as e_fallback:
#              print(f"Failed to create fallback stream logger: {e_fallback}")


# # ======================================================================================
# # CACHE PERSISTENCE HELPERS
# # ======================================================================================
# CACHE_FILE = "cache.json"
# cache_lock = threading.RLock()

# def save_cache_to_disk(cache: dict):
#     with cache_lock:
#         try:
#             serializable_cache = {}
#             logger.debug(f"Attempting to save {len(cache)} cache entries")
#             for key, value in cache.items():
#                 serializable_cache[key] = value
#             with open(CACHE_FILE, "w", encoding='utf-8') as f:
#                 json.dump(serializable_cache, f, indent=4)
#             logger.info(f"Cache saved to {CACHE_FILE} with {len(serializable_cache)} entries")
#         except Exception as e:
#             logger.error(f"Error saving cache to disk: {e}", exc_info=True)

# def load_cache_from_disk() -> dict:
#     with cache_lock:
#         if not os.path.exists(CACHE_FILE):
#             logger.info("No existing cache file found, starting fresh.")
#             return {}
#         try:
#             with open(CACHE_FILE, "r", encoding='utf-8') as f:
#                 content = f.read()
#                 if not content:
#                     logger.info("Cache file is empty, starting fresh.")
#                     return {}
#                 loaded_data = json.loads(content)
#                 logger.info(f"Loaded {len(loaded_data)} cache entries from {CACHE_FILE}")
                
#                 valid_entries = {}
#                 for canonical_key, scene_data in loaded_data.items():
#                     # We now only store English, so audio check is for English audio
#                     if isinstance(scene_data, dict) and "story_part" in scene_data:
#                         video_valid = "video_url" in scene_data and scene_data["video_url"] and os.path.exists(scene_data["video_url"].replace("/videos/", "videos/"))
#                         audio_valid = "audio_url" in scene_data and scene_data["audio_url"] and os.path.exists(scene_data["audio_url"].replace("/audio/", "audio/"))
                        
#                         if video_valid and audio_valid:
#                             valid_entries[canonical_key] = scene_data
#                             logger.debug(f"✓ Valid cache entry: '{canonical_key[:50]}...'")
#                         else:
#                             logger.warning(f"✗ Missing files for cache entry: {canonical_key[:50]}")
#                     else:
#                          logger.warning(f"✗ Skipping non-dict/invalid cache entry: {canonical_key[:50]}")

#                 logger.info(f"Restored {len(valid_entries)} valid cache entries")
#                 return valid_entries
#         except (json.JSONDecodeError, IOError) as e:
#             logger.error(f"Could not load cache from disk: {e}", exc_info=True)
#             return {}


# # ======================================================================================
# # CONFIGURATION
# # ======================================================================================
# PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
# if not PROJECT_ID: raise ValueError("GOOGLE_PROJECT_ID environment variable must be set.")
# LOCATION = os.getenv("GOOGLE_LOCATION", "us-central1")
# SERVICE_ACCOUNT_JSON = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
# if SERVICE_ACCOUNT_JSON: os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SERVICE_ACCOUNT_JSON
# CORS_ORIGINS_STR = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173")
# CORS_ORIGINS = [origin.strip() for origin in CORS_ORIGINS_STR.split(',')]
# logger.info(f"Loaded CORS allowed origins: {CORS_ORIGINS}")
# GEMINI_MODEL = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-pro")
# VEO_MODEL = os.getenv("VEO_MODEL_NAME", "veo-3.0-generate-preview")
# SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
# SERVER_PORT = int(os.getenv("SERVER_PORT", 8000))
# STOP_WORDS = set([
#     "a", "an", "the", "in", "on", "at", "with", "to", "for", "of", "from",
#     "is", "are", "was", "were", "be", "been", "being",
#     "and", "or", "but", "if", "so", "then", "about", "by", "what", "where",
#     "who", "when", "why", "how", "make", "create", "story", "about",
#     "एक", "आणि", "मध्ये", "वर", "येथे", "सह", "ते", "साठी", "चे", "पासून",
#     "आहे", "आहेत", "होता", "होते", "असणे", "असल्याने",
#     "किंवा", "पण", "जर", "म्हणून", "नंतर", "बद्दल", "काय", "कुठे",
#     "कोण", "कधी", "का", "कसे", "करा", "तयार", "कथा", "गोष्ट"
# ])


# # ======================================================================================
# # INITIALIZE APP & MIDDLEWARE
# # ======================================================================================
# app = FastAPI(title="AI Cartoon Story Builder API")
# @app.middleware("http")
# async def log_requests(request: Request, call_next):
#     start_time = time.time()
#     logger.info(f"Request: {request.method} {request.url.path} - Origin: {request.headers.get('origin')}")
#     response = await call_next(request)
#     duration = time.time() - start_time
#     logger.info(f"Response: {response.status_code} ({duration:.2f}s) - Access-Control-Allow-Origin: {response.headers.get('access-control-allow-origin')}")
#     return response
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=CORS_ORIGINS,
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"],
#     allow_headers=["*"],
# )
# os.makedirs("videos", exist_ok=True)
# os.makedirs("audio", exist_ok=True)


# # ======================================================================================
# # INITIALIZE GOOGLE CLOUD CLIENTS
# # ======================================================================================
# vertex_client = None
# tts_client = None
# translate_client = None
# client_error = None
# spell = None
# try:
#     logger.info("Initializing Google Cloud Clients...")
#     vertex_client = Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
#     tts_client = texttospeech.TextToSpeechClient()
#     translate_client = translate.Client()
#     logger.info("Google Cloud Clients initialized successfully!")
# except Exception as e:
#     client_error = str(e)
#     logger.error(f"Error initializing Google Cloud clients: {e}", exc_info=True)
# try:
#     logger.info("Initializing Spell Checker...")
#     spell = SpellChecker()
#     logger.info("Spell Checker initialized.")
# except Exception as e:
#     logger.warning(f"Error initializing Spell Checker: {e}. Spelling correction will be disabled.")
#     spell = None


# # ======================================================================================
# # CACHING AND SESSION STORAGE
# # ======================================================================================
# story_sessions = {}
# initial_cache_data = load_cache_from_disk()
# api_content_cache = {} 
# logger.info("Restoring cache entries...")
# for canonical_key, scene_data in initial_cache_data.items():
#     api_content_cache[canonical_key] = scene_data
#     logger.debug(f"     ✓ Restored: '{canonical_key[:50]}...'")
# translated_audio_cache = {} # lang -> text_hash -> audio_url
# logger.info(f"Cache initialized with {len(api_content_cache)} items from disk (UNLIMITED MODE)")


# # ======================================================================================
# # PYDANTIC MODELS
# # ======================================================================================
# class StartStoryRequest(BaseModel):
#     initial_idea: str
#     language: Optional[str] = 'en'
# class ContinueStoryRequest(BaseModel):
#     session_id: str
#     choice: str
#     language: Optional[str] = 'en'
# class ResetStoryRequest(BaseModel):
#     session_id: Optional[str] = None
# class StoryPartResponse(BaseModel):
#     scene_description: str
#     story_text: str
#     question: str
#     choices: List[str]

# class TranslateRequest(BaseModel):
#     text: str
#     target_lang: str


# # ======================================================================================
# # HELPER FUNCTIONS
# # ======================================================================================

# def normalize_prompt_for_cache(prompt: str) -> str:
#     # (Unchanged)
#     if not prompt:
#         return ""
#     words = prompt.lower().strip().split()
#     punctuation_to_strip = ".,!?'\"।" 
#     significant_words = [
#         word.strip(punctuation_to_strip) for word in words if word not in STOP_WORDS
#     ]
#     significant_words.sort()
#     canonical_key = " ".join(significant_words)
#     if not canonical_key:
#         words_stripped = [word.strip(punctuation_to_strip) for word in words]
#         words_stripped_filtered = [word for word in words_stripped if word]
#         words_stripped_filtered.sort()
#         return " ".join(words_stripped_filtered)
#     return canonical_key

# PROMPT_TO_VIDEO_KEY_MAP = {
#     # (Unchanged)
#     normalize_prompt_for_cache("sun with the moon"): normalize_prompt_for_cache("sun with the moon"),
#     normalize_prompt_for_cache("a brave knight and friendly dragon"): normalize_prompt_for_cache("a brave knight and friendly dragon"),
#     normalize_prompt_for_cache("a tortoise and rabbit"): normalize_prompt_for_cache("a tortoise and rabbit"),
#     normalize_prompt_for_cache("a little girl and bear"): normalize_prompt_for_cache("a little girl and bear"),
#     normalize_prompt_for_cache("The Monkey and the Crocodile"): normalize_prompt_for_cache("The Monkey and the Crocodile"),
# }

# def correct_spelling(text: str) -> Optional[str]:
#     # (Unchanged)
#     if not spell: return None
#     words = text.split()
#     corrected_words = []
#     has_correction = False
#     for word in words:
#         corrected_word = spell.correction(word)
#         if corrected_word and corrected_word != word:
#             corrected_words.append(corrected_word)
#             has_correction = True
#             logger.info(f"     Spelling correction: '{word}' -> '{corrected_word}'")
#         else:
#             corrected_words.append(word)
#     if not has_correction: return None
#     corrected_words.sort()
#     corrected_key = " ".join(corrected_words)
#     if corrected_key == text: return None
#     return corrected_key

# def get_next_story_part(history: str, is_first_scene: bool = False) -> Optional[Dict]:
#     # (Unchanged - EN only)
#     logger.debug("Entering get_next_story_part (EN-only)")
#     if not vertex_client:
#         logger.error(f"AI client is not initialized. Error: {client_error}")
#         return None
#     target_language = "English" # Hardcoded
#     logger.info(f"Generating story part in {target_language}")
#     raw_text = None
#     try:
#         logger.info(f"Generating story with Gemini model: {GEMINI_MODEL}")
#         if is_first_scene:
#             system_prompt = f"""
#             You are a helpful and creative storyteller for a 7-year-old child.
#             Your goal is to create a fun, branching cartoon story. You are imaginative, safe, and positive.
#             Based on the story starter, you will generate the FIRST part of the story.
#             IMPORTANT: For the first scene, the choices should be GENERIC and reusable.
#             ***** LANGUAGE REQUIREMENT *****
#             You MUST generate your entire JSON response in {target_language}.
#             ********************************
#             You MUST respond ONLY with a single, valid JSON object and no other text.
#             The JSON object must have these keys: "scene_description", "story_text", "question", "choices".
#             The "story_text" should be a short, single sentence, perfect for narration.
#             The value for "choices" must be a JSON array of three strings - make them generic!
#             """
#         else:
#             system_prompt = f"""
#             You are a helpful and creative storyteller for a 7-year-old child.
#             Your goal is to create a fun, branching cartoon story. You are imaginative, safe, and positive.
#             Based on the story so far, you will generate the next part.
#             IMPORTANT: The choices you provide for the *next* step must ALSO be GENERIC and reusable.
#             ***** LANGUAGE REQUIREMENT *****
#             You MUST generate your entire JSON response in {target_language}.
#             ********************************
#             You MUST respond ONLY with a single, valid JSON object and no other text.
#             The JSON object must have these keys: "scene_description", "story_text", "question", "choices".
#             The "story_text" should be a short, single sentence, perfect for narration.
#             The value for "choices" must be a JSON array of three strings - make them generic!
#             """
#         full_prompt = system_prompt + "\n\nHere is the story so far:\n" + history
#         response = vertex_client.models.generate_content(
#             contents=full_prompt,
#             model=GEMINI_MODEL
#         )
#         if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
#             raw_text = response.candidates[0].content.parts[0].text
#             logger.debug(f"Raw AI response:\n{raw_text}\n")
#             json_response = raw_text.strip().replace("```json", "").replace("```", "")
#             parsed = json.loads(json_response)
#             logger.info("Successfully parsed story part")
#             return parsed
#         logger.warning("No valid response from AI model.")
#         return None
#     except json.JSONDecodeError as e:
#         logger.error(f"JSON decode error: {e}", exc_info=True)
#         logger.error(f"Raw response text:\n{raw_text}\n")
#         return None
#     except Exception as e:
#         logger.error(f"Error in get_next_story_part: {e}", exc_info=True)
#         return None

# def generate_audio_narration(text: str, unique_id: str, language: str = 'en') -> Optional[str]:
#     # (Unchanged - includes audio cache)
#     if not tts_client:
#         logger.error(f"TTS client is not initialized. Error: {client_error}")
#         return None
#     text_hash = str(abs(hash(text)))
#     if language in translated_audio_cache and text_hash in translated_audio_cache[language]:
#         cached_audio_url = translated_audio_cache[language][text_hash]
#         audio_path_check = os.path.join("audio", cached_audio_url.replace("/audio/", ""))
#         if os.path.exists(audio_path_check):
#             logger.info(f"✅ Audio cache hit for {language}: {text[:30]}...")
#             return cached_audio_url
#         else:
#             logger.warning(f"Audio cache miss (file deleted) for {language}: {text[:30]}...")
#     try:
#         audio_filename = f"{language}_{unique_id}.mp3"
#         audio_path = os.path.join("audio", audio_filename)
#         if os.path.exists(audio_path):
#              logger.info(f"Audio file already exists: {audio_path}")
#              return f"/audio/{audio_filename}"
#         if language == 'mr':
#             lang_code = "mr-IN"
#             voice_name = "mr-IN-Wavenet-B" 
#             logger.info(f"Generating Marathi audio narration for text: {text[:50]}...")
#         else:
#             lang_code = "en-US"
#             voice_name = "en-US-Neural2-C" 
#             logger.info(f"Generating English audio narration for text: {text[:50]}...")
#         synthesis_input = texttospeech.SynthesisInput(text=text)
#         voice = texttospeech.VoiceSelectionParams(language_code=lang_code, name=voice_name)
#         audio_config = texttospeech.AudioConfig(
#             audio_encoding=texttospeech.AudioEncoding.MP3,
#             speaking_rate=0.95,
#             pitch=2.0
#         )
#         response = tts_client.synthesize_speech(
#             input=synthesis_input,
#             voice=voice,
#             audio_config=audio_config
#         )
#         with open(audio_path, "wb") as out:
#             out.write(response.audio_content)
#         logger.info(f"Audio saved: {audio_path}")
#         audio_url = f"/audio/{audio_filename}"
#         if language not in translated_audio_cache:
#             translated_audio_cache[language] = {}
#         translated_audio_cache[language][text_hash] = audio_url
#         return audio_url
#     except Exception as e:
#         logger.error(f"Error generating audio: {e}", exc_info=True)
#         return None

# def translate_text(text: str, target_language: str, source_language: Optional[str] = None) -> str:
#     # (Unchanged - This is the "smart" version from before)
#     """
#     Handles translation.
#     - If source_language is provided, it uses it.
#     - If not, it lets the API auto-detect the source.
#     """
#     if not translate_client:
#         logger.warning("Translate client not initialized. Returning original text.")
#         return text
#     if not text:
#         return text

#     try:
#         logger.debug(f"Translating: '{text[:50]}...' -> '{target_language}' (Source: {source_language or 'auto'})")
        
#         if source_language:
#              result = translate_client.translate(text, target_language=target_language, source_language=source_language)
#         else:
#              # This is used when we truly don't know the source
#              result = translate_client.translate(text, target_language=target_language)
        
#         translated = result['translatedText']
#         logger.debug(f"Translation result: '{translated[:50]}...'")
#         return translated
        
#     except Exception as e:
#         logger.error(f"Error during translation: {e}", exc_info=True)
#         return text # Return original text on failure


# def translate_story_part(story_part: Dict, target_language: str) -> Dict:
#     # (Unchanged)
#     if not translate_client or target_language == 'en':
#         return story_part
#     logger.info(f"Translating story part to {target_language}...")
#     try:
#         translated_part = {
#             "scene_description": story_part["scene_description"], 
#             # We explicitly translate from 'en' here
#             "story_text": translate_text(story_part["story_text"], target_language, source_language='en'),
#             "question": translate_text(story_part["question"], target_language, source_language='en'),
#             "choices": [translate_text(choice, target_language, source_language='en') for choice in story_part["choices"]]
#         }
#         logger.info("Translation successful.")
#         return translated_part
#     except Exception as e:
#         logger.error(f"Failed to translate story part: {e}", exc_info=True)
#         return story_part

# def generate_video_scene(description: str, unique_id: str) -> Optional[str]:
#     # (Unchanged)
#     if not vertex_client:
#         logger.error(f"AI client not initialized for video. Error: {client_error}")
#         raise ConnectionError(f"AI client not initialized. Error: {client_error}")
#     video_filename = f"{unique_id}.mp4"
#     video_path = os.path.join("videos", video_filename)
#     if os.path.exists(video_path):
#         logger.info(f"✅ Video file already exists (shared cache): {video_path}")
#         return f"/videos/{video_filename}"
#     prompt = description + ", in a bright, fun, simple 3D animated cartoon style for children, vibrant colors."
#     try:
#         logger.info(f"Starting video generation for prompt: {prompt[:100]}...")
#         video_config = GenerateVideosConfig(aspect_ratio='16:9')
#         operation = vertex_client.models.generate_videos(
#             model=VEO_MODEL,
#             prompt=prompt,
#             config=video_config
#         )
#         logger.info("Video job started. Polling for completion...")
#         max_wait = 300
#         poll_interval = 10
#         for i in range(0, max_wait, poll_interval):
#             time.sleep(poll_interval)
#             refreshed_op = vertex_client.operations.get(operation)
#             logger.debug(f"     Polling... {i+poll_interval}s elapsed")
#             if refreshed_op.done:
#                 operation = refreshed_op
#                 break
#         if not operation.done:
#             logger.error(f"Video generation timeout after {max_wait}s")
#             return None
#         logger.info("Video operation completed!")
#         if operation.error:
#             logger.error(f"Video generation failed with error: {operation.error}")
#             return None
#         if operation.result and operation.result.generated_videos:
#             generated_video = operation.result.generated_videos[0]
#             video_bytes = getattr(generated_video.video, 'video_bytes', None)
#             if video_bytes:
#                 with open(video_path, "wb") as f:
#                     f.write(video_bytes)
#                 logger.info(f"Video saved: {video_path}")
#                 return f"/videos/{video_filename}"
#         logger.warning("No video generated - check operation result")
#         return None
#     except Exception as e:
#         logger.error(f"Error in generate_video_scene: {e}", exc_info=True)
#         return None

# def find_best_matching_cache_key(target_key: str) -> Optional[str]:
#     # (Unchanged)
#     target_words = set(target_key.split())
#     with cache_lock:
#         if target_key in api_content_cache:
#             logger.info(f"     ✅ Exact cache match found: '{target_key[:50]}...'")
#             return target_key
#         best_match = None
#         best_match_score = 0
#         for cache_key in api_content_cache.keys():
#             cache_words = set(cache_key.split())
#             matching_words = target_words.intersection(cache_words)
#             match_score = len(matching_words)
#             if matching_words == target_words and match_score > best_match_score:
#                 best_match = cache_key
#                 best_match_score = match_score
#                 logger.info(f"     🔍 Found partial match: '{cache_key[:50]}...' (score: {match_score})")
#     if best_match:
#         logger.info(f"     ✅ Best matching cache key: '{best_match[:50]}...'")
#         return best_match
#     return None

# def get_or_create_english_scene(
#     story_context_en: str,
#     use_last_scene_only: bool = False, 
#     is_first_scene: bool = False,
# ):
#     # (Unchanged - EN only logic)
#     if use_last_scene_only and "\n" in story_context_en:
#         context_lines = story_context_en.strip().split("\n")
#         initial_idea_line = context_lines[0]
#         if "The story starts with:" in initial_idea_line:
#             initial_idea = initial_idea_line.split("The story starts with:")[-1].strip()
#         else:
#             initial_idea = initial_idea_line
#         last_line = context_lines[-1] if context_lines else story_context_en
#         if "chose that they should:" in last_line:
#             choice = last_line.split("chose that they should:")[-1].strip()
#         else:
#             choice = last_line
#         search_context_en = f"{initial_idea} {choice}"
#     else:
#         search_context_en = story_context_en
#     logger.info(f"🔍 English Context: '{search_context_en[:100]}...'")
#     canonical_key_str = normalize_prompt_for_cache(search_context_en)
#     logger.info(f"     English Cache Key: '{canonical_key_str[:100]}...'")
#     video_canonical_key = PROMPT_TO_VIDEO_KEY_MAP.get(canonical_key_str)
#     if not video_canonical_key:
#         logger.warning(f"     Prompt not in shared map. Using EN key as video key.")
#         video_canonical_key = canonical_key_str
#     video_file_id = str(abs(hash(video_canonical_key)))
#     logger.info(f"     Shared Video Key: '{video_canonical_key[:100]}...' (ID: {video_file_id})")
#     matching_cache_key = find_best_matching_cache_key(canonical_key_str)
#     if matching_cache_key:
#         with cache_lock:
#              cached_data = api_content_cache.get(matching_cache_key)
#         if cached_data:
#             logger.info("✅✅✅ ENGLISH CACHE HIT! Returning cached content instantly!")
#             return cached_data
#     logger.info(f"❌ CACHE MISS. Proceeding with new content generation for: '{canonical_key_str[:50]}...'")
#     with cache_lock:
#         if find_best_matching_cache_key(canonical_key_str):
#              logger.info("✅✅✅ CACHE HIT! (Another thread just finished).")
#              return api_content_cache[canonical_key_str]
#     story_part = get_next_story_part(story_context_en, is_first_scene=is_first_scene)
#     if not story_part:
#         raise ValueError("Failed to generate story part from API.")
#     scene_description = story_part["scene_description"]
#     logger.info("🔄 Generating video (or finding shared file)...")
#     video_url = generate_video_scene(scene_description, video_file_id)
#     if not video_url:
#         logger.error(f"❌ VIDEO GENERATION FAILED for prompt: {scene_description}")
#         raise ValueError("Failed to generate video scene. Check app.log.")
#     logger.info("🔄 Generating ENGLISH audio narration...")
#     audio_file_id = abs(hash(story_part["story_text"]))
#     audio_url = generate_audio_narration(story_part["story_text"], str(audio_file_id), language='en')
#     scene_data = {
#         "story_part": story_part,
#         "video_url": video_url,
#         "audio_url": audio_url
#     }
#     logger.info("✅ New English content generated!")
#     with cache_lock:
#         api_content_cache[canonical_key_str] = scene_data
#     return scene_data


# # ======================================================================================
# # API ENDPOINTS
# # ======================================================================================
# @app.get("/videos/{filename}")
# async def get_video(filename: str):
#     video_path = os.path.join("videos", filename)
#     if not os.path.exists(video_path):
#         logger.error(f"File not found: {video_path}")
#         raise HTTPException(status_code=404, detail="Video file not found")
#     return FileResponse(video_path, media_type="video/mp4")

# @app.get("/audio/{filename}")
# async def get_audio(filename: str):
#     audio_path = os.path.join("audio", filename)
#     if not os.path.exists(audio_path):
#         logger.error(f"File not found: {audio_path}")
#         raise HTTPException(status_code=404, detail="Audio file not found")
#     return FileResponse(audio_path, media_type="audio/mpeg")


# @app.get("/")
# async def root():
#     return {"message": "AI Cartoon Story Builder API with TTS (Unlimited Cache)", "status": "running"}

# @app.get("/api/health")
# async def health_check():
#     return {
#         "status": "healthy",
#         "ai_client_initialized": vertex_client is not None,
#         "tts_client_initialized": tts_client is not None,
#         "translate_client_initialized": translate_client is not None,
#         "client_error": client_error,
#         "active_sessions": len(story_sessions),
#         "cache_size": len(api_content_cache),
#         "cache_mode": "unlimited"
#     }

# # --- BLOCK 2: UPDATED API endpoint for live translation ---
# @app.post("/api/translate")
# async def api_translate(request: TranslateRequest):
#     if not translate_client:
#         raise HTTPException(status_code=500, detail="Translation client not initialized.")
#     if not request.text.strip():
#         return {"translated_text": ""}
    
#     try:
#         # --- THIS IS THE FIX ---
#         # We *force* the source language to be 'en' for this specific feature.
#         # This assumes the user is typing in English to have it auto-translated.
#         source_lang = 'en'
        
#         # However, if the target is 'en', we auto-detect the source.
#         if request.target_lang == 'en':
#             source_lang = None 
        
#         translated_text = await run_in_threadpool(
#             translate_text,
#             request.text,
#             request.target_lang,
#             source_language=source_lang 
#         )
#         return {"translated_text": translated_text}
#     except Exception as e:
#         logger.error(f"Error in /api/translate: {e}", exc_info=True)
#         raise HTTPException(status_code=500, detail=f"Translation failed: {e}")
# # --- END OF BLOCK 2 ---


# @app.post("/api/start-story")
# async def start_story(request: StartStoryRequest, background_tasks: BackgroundTasks):
#     # (Unchanged)
#     logger.info(f"🚀 START STORY REQUEST: '{request.initial_idea}' in lang '{request.language}'")
#     if not vertex_client:
#         raise HTTPException(status_code=500, detail=f"AI client not initialized. Error: {client_error}")
#     try:
#         session_id = f"session_{int(time.time())}"
#         initial_idea_text_en = request.initial_idea.strip()
#         if request.language != 'en':
#             # Translate to 'en', let API auto-detect source
#             initial_idea_text_en = await run_in_threadpool(translate_text, initial_idea_text_en, 'en', source_language=None)
#             logger.info(f"     Translated initial idea to EN: '{initial_idea_text_en}'")
#         if not initial_idea_text_en:
#              raise HTTPException(status_code=400, detail="Initial idea cannot be empty.")
#         corrected_context = correct_spelling(initial_idea_text_en)
#         if corrected_context:
#             initial_idea_text_en = corrected_context
#         start_time = time.time()
#         scene_data_en = await run_in_threadpool(
#             get_or_create_english_scene,
#             story_context_en=initial_idea_text_en,
#             use_last_scene_only=False, 
#             is_first_scene=True
#         )
#         background_tasks.add_task(save_cache_to_disk, api_content_cache)
#         final_story_part = scene_data_en["story_part"]
#         video_url = scene_data_en["video_url"]
#         audio_url = scene_data_en["audio_url"]
#         if request.language != 'en':
#             logger.info(f"     Translating story part to {request.language}...")
#             final_story_part = await run_in_threadpool(
#                 translate_story_part,
#                 scene_data_en["story_part"],
#                 request.language
#             )
#             logger.info(f"     Generating {request.language} audio...")
#             audio_file_id = abs(hash(final_story_part["story_text"]))
#             audio_url = await run_in_threadpool(
#                 generate_audio_narration,
#                 final_story_part["story_text"], 
#                 str(audio_file_id), 
#                 request.language
#             )
#         elapsed_time = time.time() - start_time
#         logger.info(f"⏱️ Request completed in {elapsed_time:.2f} seconds")
#         story_sessions[session_id] = {
#             "history_en": [f"The story starts with: {initial_idea_text_en}"],
#             "current_part_en": scene_data_en["story_part"]
#         }
#         return {
#             "session_id": session_id,
#             "story_part": final_story_part,
#             "video_url": video_url,
#             "audio_url": audio_url
#         }
#     except Exception as e:
#         logger.error(f"❌ Unexpected error in start_story: {e}", exc_info=True)
#         raise HTTPException(status_code=500, detail=f"Failed to start story. {e}")


# @app.post("/api/continue-story")
# async def continue_story(request: ContinueStoryRequest, background_tasks: BackgroundTasks):
#     # (Unchanged)
#     logger.info(f"➡️ CONTINUE STORY REQUEST for session {request.session_id} in lang '{request.language}'")
#     session = story_sessions.get(request.session_id)
#     if not session:
#         raise HTTPException(status_code=404, detail="Active story session not found.")
#     try:
#         choice_text_en = request.choice
#         if request.language != 'en':
#             translated_choices = [
#                 await run_in_threadpool(translate_text, c, request.language, source_language='en') 
#                 for c in session["current_part_en"]["choices"]
#             ]
#             try:
#                 choice_index = translated_choices.index(request.choice)
#                 choice_text_en = session["current_part_en"]["choices"][choice_index]
#                 logger.info(f"     Mapped choice '{request.choice}' to EN '{choice_text_en}'")
#             except ValueError:
#                 logger.warning(f"     Could not map choice '{request.choice}'. Translating back to EN.")
#                 choice_text_en = await run_in_threadpool(translate_text, request.choice, 'en', source_language=None)
#         session["history_en"].append(f"Then, the child chose that they should: {choice_text_en}")
#         story_context_en = "\n".join(session["history_en"])
#         start_time = time.time()
#         scene_data_en = await run_in_threadpool(
#             get_or_create_english_scene,
#             story_context_en=story_context_en,
#             use_last_scene_only=True, 
#             is_first_scene=False
#         )
#         background_tasks.add_task(save_cache_to_disk, api_content_cache)
#         final_story_part = scene_data_en["story_part"]
#         video_url = scene_data_en["video_url"]
#         audio_url = scene_data_en["audio_url"]
#         if request.language != 'en':
#             logger.info(f"     Translating story part to {request.language}...")
#             final_story_part = await run_in_threadpool(
#                 translate_story_part,
#                 scene_data_en["story_part"],
#                 request.language
#             )
#             logger.info(f"     Generating {request.language} audio...")
#             audio_file_id = abs(hash(final_story_part["story_text"]))
#             audio_url = await run_in_threadpool(
#                 generate_audio_narration,
#                 final_story_part["story_text"], 
#                 str(audio_file_id), 
#                 request.language
#             )
#         elapsed_time = time.time() - start_time
#         logger.info(f"⏱️ Request completed in {elapsed_time:.2f} seconds")
#         session["current_part_en"] = scene_data_en["story_part"]
#         return {
#             "story_part": final_story_part,
#             "video_url": video_url,
#             "audio_url": audio_url
#         }
#     except Exception as e:
#         logger.error(f"❌ Unexpected error in continue_story: {e}", exc_info=True)
#         raise HTTPException(status_code=500, detail=f"Failed to continue story. {e}")


# @app.post("/api/reset")
# async def reset_story(request: ResetStoryRequest):
#     # (Unchanged)
#     if request.session_id and request.session_id in story_sessions:
#         del story_sessions[request.session_id]
#         logger.info(f"🔄 Story session reset: {request.session_id}")
#         return {"message": f"Story session {request.session_id} reset successfully"}
#     if not request.session_id:
#         logger.info("🔄 All story sessions reset")
#         story_sessions.clear()
#         return {"message": "All stories reset successfully"}
#     logger.info("No active session to reset")
#     return {"message": "No active session to reset"}


# # ======================================================================================
# # RUN SERVER
# # ======================================================================================
# # --- This block is commented out as requested ---
# # if __name__ == "__main__":
# #     import uvicorn
# #     logger.info(f"\n{'='*60}")
# #     logger.info(f"🚀 Starting AI Cartoon Story Builder API with TTS (Unlimited Cache)")
# #     logger.info(f"     Host: {SERVER_HOST}")
# #     logger.info(f"     Port: {SERVER_PORT}")
# #     logger.info(f"{'='*60}\n")
    
# #     # Remember to use log_config=None to see your custom logs!
# #     uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT, log_config=None)





# # #... deployed code
# # from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
# # from fastapi.middleware.cors import CORSMiddleware
# # from fastapi.staticfiles import StaticFiles
# # from fastapi.concurrency import run_in_threadpool
# # from fastapi.responses import FileResponse
# # from pydantic import BaseModel
# # import os
# # import time
# # import json
# # import traceback
# # import threading
# # from typing import List, Dict, Optional
# # import logging
# # import sys


# # # For AI and Cloud services
# # from google.genai import Client
# # from google.genai.types import GenerateVideosConfig
# # from google.cloud import texttospeech
# # from google.cloud import translate_v2 as translate
# # from dotenv import load_dotenv

# # # For Spelling Correction
# # from spellchecker import SpellChecker


# # load_dotenv()

# # # ======================================================================================
# # # LOGGING CONFIGURATION
# # # ======================================================================================
# # log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
# # logger = logging.getLogger()
# # logger.setLevel(logging.INFO) 

# # # --- FileHandler block is commented out as requested ---
# # # try:
# # #     file_handler = logging.FileHandler("app.log", encoding='utf-8')
# # #     file_handler.setFormatter(log_formatter)
# # #     logger.addHandler(file_handler)
# # # except Exception as e:
# # #     print(f"Failed to create file logger: {e}")
# # # --- END OF CHANGE ---

# # try:
# #     stream_handler = logging.StreamHandler(sys.stdout)
# #     stream_handler.setFormatter(log_formatter)
# #     if sys.version_info >= (3, 10):
# #         stream_handler.setEncoding('utf-8')
# #     logger.addHandler(stream_handler)
# # except Exception as e:
# #     print(f"Failed to create stream logger: {e}")
# #     if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
# #         try:
# #             logger.addHandler(logging.StreamHandler(sys.stdout))
# #             logger.warning("StreamHandler UTF-8 encoding failed (likely < Python 3.10). Emojis may not display correctly in console.")
# #         except Exception as e_fallback:
# #              print(f"Failed to create fallback stream logger: {e_fallback}")


# # # ======================================================================================
# # # CACHE PERSISTENCE HELPERS
# # # ======================================================================================
# # CACHE_FILE = "cache.json"
# # cache_lock = threading.RLock()

# # def save_cache_to_disk(cache: dict):
# #     with cache_lock:
# #         try:
# #             serializable_cache = {}
# #             logger.debug(f"Attempting to save {len(cache)} cache entries")
# #             for key, value in cache.items():
# #                 serializable_cache[key] = value
# #             with open(CACHE_FILE, "w", encoding='utf-8') as f:
# #                 json.dump(serializable_cache, f, indent=4)
# #             logger.info(f"Cache saved to {CACHE_FILE} with {len(serializable_cache)} entries")
# #         except Exception as e:
# #             logger.error(f"Error saving cache to disk: {e}", exc_info=True)

# # def load_cache_from_disk() -> dict:
# #     with cache_lock:
# #         if not os.path.exists(CACHE_FILE):
# #             logger.info("No existing cache file found, starting fresh.")
# #             return {}
# #         try:
# #             with open(CACHE_FILE, "r", encoding='utf-8') as f:
# #                 content = f.read()
# #                 if not content:
# #                     logger.info("Cache file is empty, starting fresh.")
# #                     return {}
# #                 loaded_data = json.loads(content)
# #                 logger.info(f"Loaded {len(loaded_data)} cache entries from {CACHE_FILE}")
                
# #                 valid_entries = {}
# #                 for canonical_key, scene_data in loaded_data.items():
# #                     # We now only store English, so audio check is for English audio
# #                     if isinstance(scene_data, dict) and "story_part" in scene_data:
# #                         video_valid = "video_url" in scene_data and scene_data["video_url"] and os.path.exists(scene_data["video_url"].replace("/videos/", "videos/"))
# #                         audio_valid = "audio_url" in scene_data and scene_data["audio_url"] and os.path.exists(scene_data["audio_url"].replace("/audio/", "audio/"))
                        
# #                         if video_valid and audio_valid:
# #                             valid_entries[canonical_key] = scene_data
# #                             logger.debug(f"✓ Valid cache entry: '{canonical_key[:50]}...'")
# #                         else:
# #                             logger.warning(f"✗ Missing files for cache entry: {canonical_key[:50]}")
# #                     else:
# #                          logger.warning(f"✗ Skipping non-dict/invalid cache entry: {canonical_key[:50]}")

# #                 logger.info(f"Restored {len(valid_entries)} valid cache entries")
# #                 return valid_entries
# #         except (json.JSONDecodeError, IOError) as e:
# #             logger.error(f"Could not load cache from disk: {e}", exc_info=True)
# #             return {}


# # # ======================================================================================
# # # CONFIGURATION
# # # ======================================================================================
# # PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
# # if not PROJECT_ID: raise ValueError("GOOGLE_PROJECT_ID environment variable must be set.")
# # LOCATION = os.getenv("GOOGLE_LOCATION", "us-central1")
# # SERVICE_ACCOUNT_JSON = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
# # if SERVICE_ACCOUNT_JSON: os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SERVICE_ACCOUNT_JSON
# # CORS_ORIGINS_STR = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173")
# # CORS_ORIGINS = [origin.strip() for origin in CORS_ORIGINS_STR.split(',')]
# # logger.info(f"Loaded CORS allowed origins: {CORS_ORIGINS}")
# # GEMINI_MODEL = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-pro")
# # VEO_MODEL = os.getenv("VEO_MODEL_NAME", "veo-3.0-generate-preview")
# # SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
# # SERVER_PORT = int(os.getenv("SERVER_PORT", 8000))
# # STOP_WORDS = set([
# #     "a", "an", "the", "in", "on", "at", "with", "to", "for", "of", "from",
# #     "is", "are", "was", "were", "be", "been", "being",
# #     "and", "or", "but", "if", "so", "then", "about", "by", "what", "where",
# #     "who", "when", "why", "how", "make", "create", "story", "about",
# #     "एक", "आणि", "मध्ये", "वर", "येथे", "सह", "ते", "साठी", "चे", "पासून",
# #     "आहे", "आहेत", "होता", "होते", "असणे", "असल्याने",
# #     "किंवा", "पण", "जर", "म्हणून", "नंतर", "बद्दल", "काय", "कुठे",
# #     "कोण", "कधी", "का", "कसे", "करा", "तयार", "कथा", "गोष्ट"
# # ])


# # # ======================================================================================
# # # INITIALIZE APP & MIDDLEWARE
# # # ======================================================================================
# # app = FastAPI(title="AI Cartoon Story Builder API")
# # @app.middleware("http")
# # async def log_requests(request: Request, call_next):
# #     start_time = time.time()
# #     logger.info(f"Request: {request.method} {request.url.path} - Origin: {request.headers.get('origin')}")
# #     response = await call_next(request)
# #     duration = time.time() - start_time
# #     logger.info(f"Response: {response.status_code} ({duration:.2f}s) - Access-Control-Allow-Origin: {response.headers.get('access-control-allow-origin')}")
# #     return response
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=CORS_ORIGINS,
# #     allow_credentials=True,
# #     allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"],
# #     allow_headers=["*"],
# # )
# # os.makedirs("videos", exist_ok=True)
# # os.makedirs("audio", exist_ok=True)


# # # ======================================================================================
# # # INITIALIZE GOOGLE CLOUD CLIENTS
# # # ======================================================================================
# # vertex_client = None
# # tts_client = None
# # translate_client = None
# # client_error = None
# # spell = None
# # try:
# #     logger.info("Initializing Google Cloud Clients...")
# #     vertex_client = Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
# #     tts_client = texttospeech.TextToSpeechClient()
# #     translate_client = translate.Client()
# #     logger.info("Google Cloud Clients initialized successfully!")
# # except Exception as e:
# #     client_error = str(e)
# #     logger.error(f"Error initializing Google Cloud clients: {e}", exc_info=True)
# # try:
# #     logger.info("Initializing Spell Checker...")
# #     spell = SpellChecker()
# #     logger.info("Spell Checker initialized.")
# # except Exception as e:
# #     logger.warning(f"Error initializing Spell Checker: {e}. Spelling correction will be disabled.")
# #     spell = None


# # # ======================================================================================
# # # CACHING AND SESSION STORAGE
# # # ======================================================================================
# # story_sessions = {}
# # initial_cache_data = load_cache_from_disk()
# # api_content_cache = {} 
# # logger.info("Restoring cache entries...")
# # for canonical_key, scene_data in initial_cache_data.items():
# #     api_content_cache[canonical_key] = scene_data
# #     logger.debug(f"     ✓ Restored: '{canonical_key[:50]}...'")
# # translated_audio_cache = {} # lang -> text_hash -> audio_url
# # logger.info(f"Cache initialized with {len(api_content_cache)} items from disk (UNLIMITED MODE)")


# # # ======================================================================================
# # # PYDANTIC MODELS
# # # ======================================================================================
# # class StartStoryRequest(BaseModel):
# #     initial_idea: str
# #     language: Optional[str] = 'en'
# # class ContinueStoryRequest(BaseModel):
# #     session_id: str
# #     choice: str
# #     language: Optional[str] = 'en'
# # class ResetStoryRequest(BaseModel):
# #     session_id: Optional[str] = None
# # class StoryPartResponse(BaseModel):
# #     scene_description: str
# #     story_text: str
# #     question: str
# #     choices: List[str]

# # class TranslateRequest(BaseModel):
# #     text: str
# #     target_lang: str


# # # ======================================================================================
# # # HELPER FUNCTIONS
# # # ======================================================================================

# # def normalize_prompt_for_cache(prompt: str) -> str:
# #     # (Unchanged)
# #     if not prompt:
# #         return ""
# #     words = prompt.lower().strip().split()
# #     punctuation_to_strip = ".,!?'\"।" 
# #     significant_words = [
# #         word.strip(punctuation_to_strip) for word in words if word not in STOP_WORDS
# #     ]
# #     significant_words.sort()
# #     canonical_key = " ".join(significant_words)
# #     if not canonical_key:
# #         words_stripped = [word.strip(punctuation_to_strip) for word in words]
# #         words_stripped_filtered = [word for word in words_stripped if word]
# #         words_stripped_filtered.sort()
# #         return " ".join(words_stripped_filtered)
# #     return canonical_key


# # # ======================================================================================
# # # *** BEGIN BACKEND FIX ***
# # # ======================================================================================

# # # --- SOLUTION: Define a shared key for related prompts ---
# # SHARED_SUN_MOON_KEY = normalize_prompt_for_cache("sun and moon")
# # # ---

# # PROMPT_TO_VIDEO_KEY_MAP = {
# #     # --- SOLUTION: Map all variations to the *same* key ---
# #     normalize_prompt_for_cache("sun with the moon"): SHARED_SUN_MOON_KEY,
# #     normalize_prompt_for_cache("sun and moon"): SHARED_SUN_MOON_KEY,
# #     normalize_prompt_for_cache("Sunny the Sun and Luna"): SHARED_SUN_MOON_KEY,
# #     normalize_prompt_for_cache("The Sun and the Moon"): SHARED_SUN_MOON_KEY,
# #     # ---
    
# #     normalize_prompt_for_cache("a brave knight and friendly dragon"): normalize_prompt_for_cache("a brave knight and friendly dragon"),
# #     normalize_prompt_for_cache("a tortoise and rabbit"): normalize_prompt_for_cache("a tortoise and rabbit"),
# #     normalize_prompt_for_cache("a little girl and bear"): normalize_prompt_for_cache("a little girl and bear"),
# #     normalize_prompt_for_cache("The Monkey and the Crocodile"): normalize_prompt_for_cache("The Monkey and the Crocodile"),
# # }

# # # ======================================================================================
# # # *** END BACKEND FIX ***
# # # ======================================================================================


# # def correct_spelling(text: str) -> Optional[str]:
# #     # (Unchanged)
# #     if not spell: return None
# #     words = text.split()
# #     corrected_words = []
# #     has_correction = False
# #     for word in words:
# #         corrected_word = spell.correction(word)
# #         if corrected_word and corrected_word != word:
# #             corrected_words.append(corrected_word)
# #             has_correction = True
# #             logger.info(f"     Spelling correction: '{word}' -> '{corrected_word}'")
# #         else:
# #             corrected_words.append(word)
# #     if not has_correction: return None
# #     corrected_words.sort()
# #     corrected_key = " ".join(corrected_words)
# #     if corrected_key == text: return None
# #     return corrected_key

# # def get_next_story_part(history: str, is_first_scene: bool = False) -> Optional[Dict]:
# #     # (Unchanged - EN only)
# #     logger.debug("Entering get_next_story_part (EN-only)")
# #     if not vertex_client:
# #         logger.error(f"AI client is not initialized. Error: {client_error}")
# #         return None
# #     target_language = "English" # Hardcoded
# #     logger.info(f"Generating story part in {target_language}")
# #     raw_text = None
# #     try:
# #         logger.info(f"Generating story with Gemini model: {GEMINI_MODEL}")
# #         if is_first_scene:
# #             system_prompt = f"""
# #             You are a helpful and creative storyteller for a 7-year-old child.
# #             Your goal is to create a fun, branching cartoon story. You are imaginative, safe, and positive.
# #             Based on the story starter, you will generate the FIRST part of the story.
# #             IMPORTANT: For the first scene, the choices should be GENERIC and reusable.
# #             ***** LANGUAGE REQUIREMENT *****
# #             You MUST generate your entire JSON response in {target_language}.
# #             ********************************
# #             You MUST respond ONLY with a single, valid JSON object and no other text.
# #             The JSON object must have these keys: "scene_description", "story_text", "question", "choices".
# #             The "story_text" should be a short, single sentence, perfect for narration.
# #             The value for "choices" must be a JSON array of three strings - make them generic!
# #             """
# #         else:
# #             system_prompt = f"""
# #             You are a helpful and creative storyteller for a 7-year-old child.
# #             Your goal is to create a fun, branching cartoon story. You are imaginative, safe, and positive.
# #             Based on the story so far, you will generate the next part.
# #             IMPORTANT: The choices you provide for the *next* step must ALSO be GENERIC and reusable.
# #             ***** LANGUAGE REQUIREMENT *****
# #             You MUST generate your entire JSON response in {target_language}.
# #             ********************************
# #             You MUST respond ONLY with a single, valid JSON object and no other text.
# #             The JSON object must have these keys: "scene_description", "story_text", "question", "choices".
# #             The "story_text" should be a short, single sentence, perfect for narration.
# #             The value for "choices" must be a JSON array of three strings - make them generic!
# #             """
# #         full_prompt = system_prompt + "\n\nHere is the story so far:\n" + history
# #         response = vertex_client.models.generate_content(
# #             contents=full_prompt,
# #             model=GEMINI_MODEL
# #         )
# #         if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
# #             raw_text = response.candidates[0].content.parts[0].text
# #             logger.debug(f"Raw AI response:\n{raw_text}\n")
# #             json_response = raw_text.strip().replace("```json", "").replace("```", "")
# #             parsed = json.loads(json_response)
# #             logger.info("Successfully parsed story part")
# #             return parsed
# #         logger.warning("No valid response from AI model.")
# #         return None
# #     except json.JSONDecodeError as e:
# #         logger.error(f"JSON decode error: {e}", exc_info=True)
# #         logger.error(f"Raw response text:\n{raw_text}\n")
# #         return None
# #     except Exception as e:
# #         logger.error(f"Error in get_next_story_part: {e}", exc_info=True)
# #         return None

# # def generate_audio_narration(text: str, unique_id: str, language: str = 'en') -> Optional[str]:
# #     # (Unchanged - includes audio cache)
# #     if not tts_client:
# #         logger.error(f"TTS client is not initialized. Error: {client_error}")
# #         return None
# #     text_hash = str(abs(hash(text)))
# #     if language in translated_audio_cache and text_hash in translated_audio_cache[language]:
# #         cached_audio_url = translated_audio_cache[language][text_hash]
# #         audio_path_check = os.path.join("audio", cached_audio_url.replace("/audio/", ""))
# #         if os.path.exists(audio_path_check):
# #             logger.info(f"✅ Audio cache hit for {language}: {text[:30]}...")
# #             return cached_audio_url
# #         else:
# #             logger.warning(f"Audio cache miss (file deleted) for {language}: {text[:30]}...")
# #     try:
# #         audio_filename = f"{language}_{unique_id}.mp3"
# #         audio_path = os.path.join("audio", audio_filename)
# #         if os.path.exists(audio_path):
# #              logger.info(f"Audio file already exists: {audio_path}")
# #              return f"/audio/{audio_filename}"
# #         if language == 'mr':
# #             lang_code = "mr-IN"
# #             voice_name = "mr-IN-Wavenet-B" 
# #             logger.info(f"Generating Marathi audio narration for text: {text[:50]}...")
# #         else:
# #             lang_code = "en-US"
# #             voice_name = "en-US-Neural2-C" 
# #             logger.info(f"Generating English audio narration for text: {text[:50]}...")
# #         synthesis_input = texttospeech.SynthesisInput(text=text)
# #         voice = texttospeech.VoiceSelectionParams(language_code=lang_code, name=voice_name)
# #         audio_config = texttospeech.AudioConfig(
# #             audio_encoding=texttospeech.AudioEncoding.MP3,
# #             speaking_rate=0.95,
# #             pitch=2.0
# #         )
# #         response = tts_client.synthesize_speech(
# #             input=synthesis_input,
# #             voice=voice,
# #             audio_config=audio_config
# #         )
# #         with open(audio_path, "wb") as out:
# #             out.write(response.audio_content)
# #         logger.info(f"Audio saved: {audio_path}")
# #         audio_url = f"/audio/{audio_filename}"
# #         if language not in translated_audio_cache:
# #             translated_audio_cache[language] = {}
# #         translated_audio_cache[language][text_hash] = audio_url
# #         return audio_url
# #     except Exception as e:
# #         logger.error(f"Error generating audio: {e}", exc_info=True)
# #         return None

# # def translate_text(text: str, target_language: str, source_language: Optional[str] = None) -> str:
# #     # (Unchanged - This is the "smart" version from before)
# #     """
# #     Handles translation.
# #     - If source_language is provided, it uses it.
# #     - If not, it lets the API auto-detect the source.
# #     """
# #     if not translate_client:
# #         logger.warning("Translate client not initialized. Returning original text.")
# #         return text
# #     if not text:
# #         return text

# #     try:
# #         logger.debug(f"Translating: '{text[:50]}...' -> '{target_language}' (Source: {source_language or 'auto'})")
        
# #         if source_language:
# #              result = translate_client.translate(text, target_language=target_language, source_language=source_language)
# #         else:
# #              # This is used when we truly don't know the source
# #              result = translate_client.translate(text, target_language=target_language)
        
# #         translated = result['translatedText']
# #         logger.debug(f"Translation result: '{translated[:50]}...'")
# #         return translated
        
# #     except Exception as e:
# #         logger.error(f"Error during translation: {e}", exc_info=True)
# #         return text # Return original text on failure


# # def translate_story_part(story_part: Dict, target_language: str) -> Dict:
# #     # (Unchanged)
# #     if not translate_client or target_language == 'en':
# #         return story_part
# #     logger.info(f"Translating story part to {target_language}...")
# #     try:
# #         translated_part = {
# #             "scene_description": story_part["scene_description"], 
# #             # We explicitly translate from 'en' here
# #             "story_text": translate_text(story_part["story_text"], target_language, source_language='en'),
# #             "question": translate_text(story_part["question"], target_language, source_language='en'),
# #             "choices": [translate_text(choice, target_language, source_language='en') for choice in story_part["choices"]]
# #         }
# #         logger.info("Translation successful.")
# #         return translated_part
# #     except Exception as e:
# #         logger.error(f"Failed to translate story part: {e}", exc_info=True)
# #         return story_part

# # def generate_video_scene(description: str, unique_id: str) -> Optional[str]:
# #     # (Unchanged)
# #     if not vertex_client:
# #         logger.error(f"AI client not initialized for video. Error: {client_error}")
# #         raise ConnectionError(f"AI client not initialized. Error: {client_error}")
# #     video_filename = f"{unique_id}.mp4"
# #     video_path = os.path.join("videos", video_filename)
# #     if os.path.exists(video_path):
# #         logger.info(f"✅ Video file already exists (shared cache): {video_path}")
# #         return f"/videos/{video_filename}"
# #     prompt = description + ", in a bright, fun, simple 3D animated cartoon style for children, vibrant colors."
# #     try:
# #         logger.info(f"Starting video generation for prompt: {prompt[:100]}...")
# #         video_config = GenerateVideosConfig(aspect_ratio='16:9')
# #         operation = vertex_client.models.generate_videos(
# #             model=VEO_MODEL,
# #             prompt=prompt,
# #             config=video_config
# #         )
# #         logger.info("Video job started. Polling for completion...")
# #         max_wait = 300
# #         poll_interval = 10
# #         for i in range(0, max_wait, poll_interval):
# #             time.sleep(poll_interval)
# #             refreshed_op = vertex_client.operations.get(operation)
# #             logger.debug(f"     Polling... {i+poll_interval}s elapsed")
# #             if refreshed_op.done:
# #                 operation = refreshed_op
# #                 break
# #         if not operation.done:
# #             logger.error(f"Video generation timeout after {max_wait}s")
# #             return None
# #         logger.info("Video operation completed!")
# #         if operation.error:
# #             logger.error(f"Video generation failed with error: {operation.error}")
# #             return None
# #         if operation.result and operation.result.generated_videos:
# #             generated_video = operation.result.generated_videos[0]
# #             video_bytes = getattr(generated_video.video, 'video_bytes', None)
# #             if video_bytes:
# #                 with open(video_path, "wb") as f:
# #                     f.write(video_bytes)
# #                 logger.info(f"Video saved: {video_path}")
# #                 return f"/videos/{video_filename}"
# #         logger.warning("No video generated - check operation result")
# #         return None
# #     except Exception as e:
# #         logger.error(f"Error in generate_video_scene: {e}", exc_info=True)
# #         return None

# # def find_best_matching_cache_key(target_key: str) -> Optional[str]:
# #     # (Unchanged)
# #     target_words = set(target_key.split())
# #     with cache_lock:
# #         if target_key in api_content_cache:
# #             logger.info(f"     ✅ Exact cache match found: '{target_key[:50]}...'")
# #             return target_key
# #         best_match = None
# #         best_match_score = 0
# #         for cache_key in api_content_cache.keys():
# #             cache_words = set(cache_key.split())
# #             matching_words = target_words.intersection(cache_words)
# #             match_score = len(matching_words)
# #             if matching_words == target_words and match_score > best_match_score:
# #                 best_match = cache_key
# #                 best_match_score = match_score
# #                 logger.info(f"     🔍 Found partial match: '{cache_key[:50]}...' (score: {match_score})")
# #     if best_match:
# #         logger.info(f"     ✅ Best matching cache key: '{best_match[:50]}...'")
# #         return best_match
# #     return None

# # def get_or_create_english_scene(
# #     story_context_en: str,
# #     use_last_scene_only: bool = False, 
# #     is_first_scene: bool = False,
# # ):
# #     # (Unchanged - EN only logic)
# #     if use_last_scene_only and "\n" in story_context_en:
# #         context_lines = story_context_en.strip().split("\n")
# #         initial_idea_line = context_lines[0]
# #         if "The story starts with:" in initial_idea_line:
# #             initial_idea = initial_idea_line.split("The story starts with:")[-1].strip()
# #         else:
# #             initial_idea = initial_idea_line
# #         last_line = context_lines[-1] if context_lines else story_context_en
# #         if "chose that they should:" in last_line:
# #             choice = last_line.split("chose that they should:")[-1].strip()
# #         else:
# #             choice = last_line
# #         search_context_en = f"{initial_idea} {choice}"
# #     else:
# #         search_context_en = story_context_en
# #     logger.info(f"🔍 English Context: '{search_context_en[:100]}...'")
# #     canonical_key_str = normalize_prompt_for_cache(search_context_en)
# #     logger.info(f"     English Cache Key: '{canonical_key_str[:100]}...'")
# #     video_canonical_key = PROMPT_TO_VIDEO_KEY_MAP.get(canonical_key_str)
# #     if not video_canonical_key:
# #         logger.warning(f"     Prompt not in shared map. Using EN key as video key.")
# #         video_canonical_key = canonical_key_str
# #     video_file_id = str(abs(hash(video_canonical_key)))
# #     logger.info(f"     Shared Video Key: '{video_canonical_key[:100]}...' (ID: {video_file_id})")
# #     matching_cache_key = find_best_matching_cache_key(canonical_key_str)
# #     if matching_cache_key:
# #         with cache_lock:
# #              cached_data = api_content_cache.get(matching_cache_key)
# #         if cached_data:
# #             logger.info("✅✅✅ ENGLISH CACHE HIT! Returning cached content instantly!")
# #             return cached_data
# #     logger.info(f"❌ CACHE MISS. Proceeding with new content generation for: '{canonical_key_str[:50]}...'")
# #     with cache_lock:
# #         if find_best_matching_cache_key(canonical_key_str):
# #              logger.info("✅✅✅ CACHE HIT! (Another thread just finished).")
# #              return api_content_cache[canonical_key_str]
# #     story_part = get_next_story_part(story_context_en, is_first_scene=is_first_scene)
# #     if not story_part:
# #         raise ValueError("Failed to generate story part from API.")
# #     scene_description = story_part["scene_description"]
# #     logger.info("🔄 Generating video (or finding shared file)...")
# #     video_url = generate_video_scene(scene_description, video_file_id)
# #     if not video_url:
# #         logger.error(f"❌ VIDEO GENERATION FAILED for prompt: {scene_description}")
# #         raise ValueError("Failed to generate video scene. Check app.log.")
# #     logger.info("🔄 Generating ENGLISH audio narration...")
# #     audio_file_id = abs(hash(story_part["story_text"]))
# #     audio_url = generate_audio_narration(story_part["story_text"], str(audio_file_id), language='en')
# #     scene_data = {
# #         "story_part": story_part,
# #         "video_url": video_url,
# #         "audio_url": audio_url
# #     }
# #     logger.info("✅ New English content generated!")
# #     with cache_lock:
# #         api_content_cache[canonical_key_str] = scene_data
# #     return scene_data


# # # ======================================================================================
# # # API ENDPOINTS
# # # ======================================================================================
# # @app.get("/videos/{filename}")
# # async def get_video(filename: str):
# #     video_path = os.path.join("videos", filename)
# #     if not os.path.exists(video_path):
# #         logger.error(f"File not found: {video_path}")
# #         raise HTTPException(status_code=404, detail="Video file not found")
# #     return FileResponse(video_path, media_type="video/mp4")

# # @app.get("/audio/{filename}")
# # async def get_audio(filename: str):
# #     audio_path = os.path.join("audio", filename)
# #     if not os.path.exists(audio_path):
# #         logger.error(f"File not found: {audio_path}")
# #         raise HTTPException(status_code=404, detail="Audio file not found")
# #     return FileResponse(audio_path, media_type="audio/mpeg")


# # @app.get("/")
# # async def root():
# #     return {"message": "AI Cartoon Story Builder API with TTS (Unlimited Cache)", "status": "running"}

# # @app.get("/api/health")
# # async def health_check():
# #     return {
# #         "status": "healthy",
# #         "ai_client_initialized": vertex_client is not None,
# #         "tts_client_initialized": tts_client is not None,
# #         "translate_client_initialized": translate_client is not None,
# #         "client_error": client_error,
# #         "active_sessions": len(story_sessions),
# #         "cache_size": len(api_content_cache),
# #         "cache_mode": "unlimited"
# #     }

# # # --- BLOCK 2: UPDATED API endpoint for live translation ---
# # @app.post("/api/translate")
# # async def api_translate(request: TranslateRequest):
# #     if not translate_client:
# #         raise HTTPException(status_code=500, detail="Translation client not initialized.")
# #     if not request.text.strip():
# #         return {"translated_text": ""}
    
# #     try:
# #         # --- THIS IS THE FIX ---
# #         # We *force* the source language to be 'en' for this specific feature.
# #         # This assumes the user is typing in English to have it auto-translated.
# #         source_lang = 'en'
        
# #         # However, if the target is 'en', we auto-detect the source.
# #         if request.target_lang == 'en':
# #             source_lang = None 
        
# #         translated_text = await run_in_threadpool(
# #             translate_text,
# #             request.text,
# #             request.target_lang,
# #             source_language=source_lang 
# #         )
# #         return {"translated_text": translated_text}
# #     except Exception as e:
# #         logger.error(f"Error in /api/translate: {e}", exc_info=True)
# #         raise HTTPException(status_code=500, detail=f"Translation failed: {e}")
# # # --- END OF BLOCK 2 ---


# # @app.post("/api/start-story")
# # async def start_story(request: StartStoryRequest, background_tasks: BackgroundTasks):
# #     # (Unchanged)
# #     logger.info(f"🚀 START STORY REQUEST: '{request.initial_idea}' in lang '{request.language}'")
# #     if not vertex_client:
# #         raise HTTPException(status_code=500, detail=f"AI client not initialized. Error: {client_error}")
# #     try:
# #         session_id = f"session_{int(time.time())}"
# #         initial_idea_text_en = request.initial_idea.strip()
# #         if request.language != 'en':
# #             # Translate to 'en', let API auto-detect source
# #             initial_idea_text_en = await run_in_threadpool(translate_text, initial_idea_text_en, 'en', source_language=None)
# #             logger.info(f"     Translated initial idea to EN: '{initial_idea_text_en}'")
# #         if not initial_idea_text_en:
# #              raise HTTPException(status_code=400, detail="Initial idea cannot be empty.")
# #         corrected_context = correct_spelling(initial_idea_text_en)
# #         if corrected_context:
# #             initial_idea_text_en = corrected_context
# #         start_time = time.time()
# #         scene_data_en = await run_in_threadpool(
# #             get_or_create_english_scene,
# #             story_context_en=initial_idea_text_en,
# #             use_last_scene_only=False, 
# #             is_first_scene=True
# #         )
# #         background_tasks.add_task(save_cache_to_disk, api_content_cache)
# #         final_story_part = scene_data_en["story_part"]
# #         video_url = scene_data_en["video_url"]
# #         audio_url = scene_data_en["audio_url"]
# #         if request.language != 'en':
# #             logger.info(f"     Translating story part to {request.language}...")
# #             final_story_part = await run_in_threadpool(
# #                 translate_story_part,
# #                 scene_data_en["story_part"],
# #                 request.language
# #             )
# #             logger.info(f"     Generating {request.language} audio...")
# #             audio_file_id = abs(hash(final_story_part["story_text"]))
# #             audio_url = await run_in_threadpool(
# #                 generate_audio_narration,
# #                 final_story_part["story_text"], 
# #                 str(audio_file_id), 
# #                 request.language
# #             )
# #         elapsed_time = time.time() - start_time
# #         logger.info(f"⏱️ Request completed in {elapsed_time:.2f} seconds")
# #         story_sessions[session_id] = {
# #             "history_en": [f"The story starts with: {initial_idea_text_en}"],
# #             "current_part_en": scene_data_en["story_part"]
# #         }
# #         return {
# #             "session_id": session_id,
# #             "story_part": final_story_part,
# #             "video_url": video_url,
# #             "audio_url": audio_url
# #         }
# #     except Exception as e:
# #         logger.error(f"❌ Unexpected error in start_story: {e}", exc_info=True)
# #         raise HTTPException(status_code=500, detail=f"Failed to start story. {e}")


# # @app.post("/api/continue-story")
# # async def continue_story(request: ContinueStoryRequest, background_tasks: BackgroundTasks):
# #     # (Unchanged)
# #     logger.info(f"➡️ CONTINUE STORY REQUEST for session {request.session_id} in lang '{request.language}'")
# #     session = story_sessions.get(request.session_id)
# #     if not session:
# #         raise HTTPException(status_code=404, detail="Active story session not found.")
# #     try:
# #         choice_text_en = request.choice
# #         if request.language != 'en':
# #             translated_choices = [
# #                 await run_in_threadpool(translate_text, c, request.language, source_language='en') 
# #                 for c in session["current_part_en"]["choices"]
# #             ]
# #             try:
# #                 choice_index = translated_choices.index(request.choice)
# #                 choice_text_en = session["current_part_en"]["choices"][choice_index]
# #                 logger.info(f"     Mapped choice '{request.choice}' to EN '{choice_text_en}'")
# #             except ValueError:
# #                 logger.warning(f"     Could not map choice '{request.choice}'. Translating back to EN.")
# #                 choice_text_en = await run_in_threadpool(translate_text, request.choice, 'en', source_language=None)
# #         session["history_en"].append(f"Then, the child chose that they should: {choice_text_en}")
# #         story_context_en = "\n".join(session["history_en"])
# #         start_time = time.time()
# #         scene_data_en = await run_in_threadpool(
# #             get_or_create_english_scene,
# #             story_context_en=story_context_en,
# #             use_last_scene_only=True, 
# #             is_first_scene=False
# #         )
# #         background_tasks.add_task(save_cache_to_disk, api_content_cache)
# #         final_story_part = scene_data_en["story_part"]
# #         video_url = scene_data_en["video_url"]
# #         audio_url = scene_data_en["audio_url"]
# #         if request.language != 'en':
# #             logger.info(f"     Translating story part to {request.language}...")
# #             final_story_part = await run_in_threadpool(
# #                 translate_story_part,
# #                 scene_data_en["story_part"],
# #                 request.language
# #             )
# #             logger.info(f"     Generating {request.language} audio...")
# #             audio_file_id = abs(hash(final_story_part["story_text"]))
# #             audio_url = await run_in_threadpool(
# #                 generate_audio_narration,
# #                 final_story_part["story_text"], 
# #                 str(audio_file_id), 
# #                 request.language
# #             )
# #         elapsed_time = time.time() - start_time
# #         logger.info(f"⏱️ Request completed in {elapsed_time:.2f} seconds")
# #         session["current_part_en"] = scene_data_en["story_part"]
# #         return {
# #             "story_part": final_story_part,
# #             "video_url": video_url,
# #             "audio_url": audio_url
# #         }
# #     except Exception as e:
# #         logger.error(f"❌ Unexpected error in continue_story: {e}", exc_info=True)
# #         raise HTTPException(status_code=500, detail=f"Failed to continue story. {e}")


# # @app.post("/api/reset")
# # async def reset_story(request: ResetStoryRequest):
# #     # (Unchanged)
# #     if request.session_id and request.session_id in story_sessions:
# #         del story_sessions[request.session_id]
# #         logger.info(f"🔄 Story session reset: {request.session_id}")
# #         return {"message": f"Story session {request.session_id} reset successfully"}
# #     if not request.session_id:
# #         logger.info("🔄 All story sessions reset")
# #         story_sessions.clear()
# #         return {"message": "All stories reset successfully"}
# #     logger.info("No active session to reset")
# #     return {"message": "No active session to reset"}


# # # ======================================================================================
# # # RUN SERVER
# # # ======================================================================================
# # # --- This block is commented out as requested ---
# # # if __name__ == "__main__":
# # #     import uvicorn
# # #     logger.info(f"\n{'='*60}")
# # #     logger.info(f"🚀 Starting AI Cartoon Story Builder API with TTS (Unlimited Cache)")
# # #     logger.info(f"     Host: {SERVER_HOST}")
# # #     logger.info(f"     Port: {SERVER_PORT}")
# # #     logger.info(f"{'='*60}\n")
    
# # #     # Remember to use log_config=None to see your custom logs!
# # #     uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT, log_config=None)


# ..updated code with audio
from fastapi import FastAPI, HTTPException, Request, BackgroundTasks, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import time
import json
import traceback
import threading
from typing import List, Dict, Optional
import logging
import sys

# For AI and Cloud services
from google.genai import Client
from google.genai.types import GenerateVideosConfig
from google.cloud import texttospeech
from google.cloud import translate_v2 as translate
from google.cloud import speech  # <-- Added for Speech-to-Text
from dotenv import load_dotenv

# For Spelling Correction
from spellchecker import SpellChecker


load_dotenv()

# ======================================================================================
# LOGGING CONFIGURATION
# ======================================================================================
log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO) 

# --- FileHandler block is commented out as requested ---
# try:
#     file_handler = logging.FileHandler("app.log", encoding='utf-8')
#     file_handler.setFormatter(log_formatter)
#     logger.addHandler(file_handler)
# except Exception as e:
#     print(f"Failed to create file logger: {e}")
# --- END OF CHANGE ---

try:
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(log_formatter)
    if sys.version_info >= (3, 10):
        stream_handler.setEncoding('utf-8')
    logger.addHandler(stream_handler)
except Exception as e:
    print(f"Failed to create stream logger: {e}")
    if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        try:
            logger.addHandler(logging.StreamHandler(sys.stdout))
            logger.warning("StreamHandler UTF-8 encoding failed (likely < Python 3.10). Emojis may not display correctly in console.")
        except Exception as e_fallback:
             print(f"Failed to create fallback stream logger: {e_fallback}")


# ======================================================================================
# CACHE PERSISTENCE HELPERS
# ======================================================================================
CACHE_FILE = "cache.json"
cache_lock = threading.RLock()

def save_cache_to_disk(cache: dict):
    with cache_lock:
        try:
            serializable_cache = {}
            logger.debug(f"Attempting to save {len(cache)} cache entries")
            for key, value in cache.items():
                serializable_cache[key] = value
            with open(CACHE_FILE, "w", encoding='utf-8') as f:
                json.dump(serializable_cache, f, indent=4)
            logger.info(f"Cache saved to {CACHE_FILE} with {len(serializable_cache)} entries")
        except Exception as e:
            logger.error(f"Error saving cache to disk: {e}", exc_info=True)

def load_cache_from_disk() -> dict:
    with cache_lock:
        if not os.path.exists(CACHE_FILE):
            logger.info("No existing cache file found, starting fresh.")
            return {}
        try:
            with open(CACHE_FILE, "r", encoding='utf-8') as f:
                content = f.read()
                if not content:
                    logger.info("Cache file is empty, starting fresh.")
                    return {}
                loaded_data = json.loads(content)
                logger.info(f"Loaded {len(loaded_data)} cache entries from {CACHE_FILE}")
                
                valid_entries = {}
                for canonical_key, scene_data in loaded_data.items():
                    # We now only store English, so audio check is for English audio
                    if isinstance(scene_data, dict) and "story_part" in scene_data:
                        video_valid = "video_url" in scene_data and scene_data["video_url"] and os.path.exists(scene_data["video_url"].replace("/videos/", "videos/"))
                        audio_valid = "audio_url" in scene_data and scene_data["audio_url"] and os.path.exists(scene_data["audio_url"].replace("/audio/", "audio/"))
                        
                        if video_valid and audio_valid:
                            valid_entries[canonical_key] = scene_data
                            logger.debug(f"✓ Valid cache entry: '{canonical_key[:50]}...'")
                        else:
                            logger.warning(f"✗ Missing files for cache entry: {canonical_key[:50]}")
                    else:
                         logger.warning(f"✗ Skipping non-dict/invalid cache entry: {canonical_key[:50]}")

                logger.info(f"Restored {len(valid_entries)} valid cache entries")
                return valid_entries
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Could not load cache from disk: {e}", exc_info=True)
            return {}


# ======================================================================================
# CONFIGURATION
# ======================================================================================
PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
if not PROJECT_ID: raise ValueError("GOOGLE_PROJECT_ID environment variable must be set.")
LOCATION = os.getenv("GOOGLE_LOCATION", "us-central1")
SERVICE_ACCOUNT_JSON = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if SERVICE_ACCOUNT_JSON: os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SERVICE_ACCOUNT_JSON
CORS_ORIGINS_STR = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173")
CORS_ORIGINS = [origin.strip() for origin in CORS_ORIGINS_STR.split(',')]
logger.info(f"Loaded CORS allowed origins: {CORS_ORIGINS}")
GEMINI_MODEL = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-pro")
VEO_MODEL = os.getenv("VEO_MODEL_NAME", "veo-3.0-generate-preview")
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", 8000))
STOP_WORDS = set([
    "a", "an", "the", "in", "on", "at", "with", "to", "for", "of", "from",
    "is", "are", "was", "were", "be", "been", "being",
    "and", "or", "but", "if", "so", "then", "about", "by", "what", "where",
    "who", "when", "why", "how", "make", "create", "story", "about",
    "एक", "आणि", "मध्ये", "वर", "येथे", "सह", "ते", "साठी", "चे", "पासून",
    "आहे", "आहेत", "होता", "होते", "असणे", "असल्याने",
    "किंवा", "पण", "जर", "म्हणून", "नंतर", "बद्दल", "काय", "कुठे",
    "कोण", "कधी", "का", "कसे", "करा", "तयार", "कथा", "गोष्ट"
])


# ======================================================================================
# INITIALIZE APP & MIDDLEWARE
# ======================================================================================
app = FastAPI(title="AI Cartoon Story Builder API")
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(f"Request: {request.method} {request.url.path} - Origin: {request.headers.get('origin')}")
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"Response: {response.status_code} ({duration:.2f}s) - Access-Control-Allow-Origin: {response.headers.get('access-control-allow-origin')}")
    return response
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"],
    allow_headers=["*"],
)
os.makedirs("videos", exist_ok=True)
os.makedirs("audio", exist_ok=True)


# ======================================================================================
# INITIALIZE GOOGLE CLOUD CLIENTS
# ======================================================================================
vertex_client = None
tts_client = None
translate_client = None
speech_client = None  # <-- Added for Speech-to-Text
client_error = None
spell = None
try:
    logger.info("Initializing Google Cloud Clients...")
    vertex_client = Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
    tts_client = texttospeech.TextToSpeechClient()
    translate_client = translate.Client()
    speech_client = speech.SpeechClient()  # <-- Initialized Speech-to-Text client
    logger.info("Google Cloud Clients initialized successfully!")
except Exception as e:
    client_error = str(e)
    logger.error(f"Error initializing Google Cloud clients: {e}", exc_info=True)
try:
    logger.info("Initializing Spell Checker...")
    spell = SpellChecker()
    logger.info("Spell Checker initialized.")
except Exception as e:
    logger.warning(f"Error initializing Spell Checker: {e}. Spelling correction will be disabled.")
    spell = None


# ======================================================================================
# CACHING AND SESSION STORAGE
# ======================================================================================
story_sessions = {}
initial_cache_data = load_cache_from_disk()
api_content_cache = {} 
logger.info("Restoring cache entries...")
for canonical_key, scene_data in initial_cache_data.items():
    api_content_cache[canonical_key] = scene_data
    logger.debug(f"     ✓ Restored: '{canonical_key[:50]}...'")
translated_audio_cache = {} # lang -> text_hash -> audio_url
logger.info(f"Cache initialized with {len(api_content_cache)} items from disk (UNLIMITED MODE)")


# ======================================================================================
# PYDANTIC MODELS
# ======================================================================================
class StartStoryRequest(BaseModel):
    initial_idea: str
    language: Optional[str] = 'en'
class ContinueStoryRequest(BaseModel):
    session_id: str
    choice: str
    language: Optional[str] = 'en'
class ResetStoryRequest(BaseModel):
    session_id: Optional[str] = None
class StoryPartResponse(BaseModel):
    scene_description: str
    story_text: str
    question: str
    choices: List[str]

class TranslateRequest(BaseModel):
    text: str
    target_lang: str


# ======================================================================================
# HELPER FUNCTIONS
# ======================================================================================

def normalize_prompt_for_cache(prompt: str) -> str:
    # (Unchanged)
    if not prompt:
        return ""
    words = prompt.lower().strip().split()
    punctuation_to_strip = ".,!?'\"।" 
    significant_words = [
        word.strip(punctuation_to_strip) for word in words if word not in STOP_WORDS
    ]
    significant_words.sort()
    canonical_key = " ".join(significant_words)
    if not canonical_key:
        words_stripped = [word.strip(punctuation_to_strip) for word in words]
        words_stripped_filtered = [word for word in words_stripped if word]
        words_stripped_filtered.sort()
        return " ".join(words_stripped_filtered)
    return canonical_key


# ======================================================================================
# *** BEGIN BACKEND FIX ***
# ======================================================================================

# --- SOLUTION: Define a shared key for related prompts ---
SHARED_SUN_MOON_KEY = normalize_prompt_for_cache("sun and moon")
# ---

PROMPT_TO_VIDEO_KEY_MAP = {
    # --- SOLUTION: Map all variations to the *same* key ---
    normalize_prompt_for_cache("sun with the moon"): SHARED_SUN_MOON_KEY,
    normalize_prompt_for_cache("sun and moon"): SHARED_SUN_MOON_KEY,
    normalize_prompt_for_cache("Sunny the Sun and Luna"): SHARED_SUN_MOON_KEY,
    normalize_prompt_for_cache("The Sun and the Moon"): SHARED_SUN_MOON_KEY,
    # ---
    
    normalize_prompt_for_cache("a brave knight and friendly dragon"): normalize_prompt_for_cache("a brave knight and friendly dragon"),
    normalize_prompt_for_cache("a tortoise and rabbit"): normalize_prompt_for_cache("a tortoise and rabbit"),
    normalize_prompt_for_cache("a little girl and bear"): normalize_prompt_for_cache("a little girl and bear"),
    normalize_prompt_for_cache("The Monkey and the Crocodile"): normalize_prompt_for_cache("The Monkey and the Crocodile"),
}

# ======================================================================================
# *** END BACKEND FIX ***
# ======================================================================================


def correct_spelling(text: str) -> Optional[str]:
    # (Unchanged)
    if not spell: return None
    words = text.split()
    corrected_words = []
    has_correction = False
    for word in words:
        corrected_word = spell.correction(word)
        if corrected_word and corrected_word != word:
            corrected_words.append(corrected_word)
            has_correction = True
            logger.info(f"     Spelling correction: '{word}' -> '{corrected_word}'")
        else:
            corrected_words.append(word)
    if not has_correction: return None
    corrected_words.sort()
    corrected_key = " ".join(corrected_words)
    if corrected_key == text: return None
    return corrected_key

def get_next_story_part(history: str, is_first_scene: bool = False) -> Optional[Dict]:
    # (Unchanged - EN only)
    logger.debug("Entering get_next_story_part (EN-only)")
    if not vertex_client:
        logger.error(f"AI client is not initialized. Error: {client_error}")
        return None
    target_language = "English" # Hardcoded
    logger.info(f"Generating story part in {target_language}")
    raw_text = None
    try:
        logger.info(f"Generating story with Gemini model: {GEMINI_MODEL}")
        if is_first_scene:
            system_prompt = f"""
            You are a helpful and creative storyteller for a 7-year-old child.
            Your goal is to create a fun, branching cartoon story. You are imaginative, safe, and positive.
            Based on the story starter, you will generate the FIRST part of the story.
            IMPORTANT: For the first scene, the choices should be GENERIC and reusable.
            ***** LANGUAGE REQUIREMENT *****
            You MUST generate your entire JSON response in {target_language}.
            ********************************
            You MUST respond ONLY with a single, valid JSON object and no other text.
            The JSON object must have these keys: "scene_description", "story_text", "question", "choices".
            The "story_text" should be a short, single sentence, perfect for narration.
            The value for "choices" must be a JSON array of three strings - make them generic!
            """
        else:
            system_prompt = f"""
            You are a helpful and creative storyteller for a 7-year-old child.
            Your goal is to create a fun, branching cartoon story. You are imaginative, safe, and positive.
            Based on the story so far, you will generate the next part.
            IMPORTANT: The choices you provide for the *next* step must ALSO be GENERIC and reusable.
            ***** LANGUAGE REQUIREMENT *****
            You MUST generate your entire JSON response in {target_language}.
            ********************************
            You MUST respond ONLY with a single, valid JSON object and no other text.
            The JSON object must have these keys: "scene_description", "story_text", "question", "choices".
            The "story_text" should be a short, single sentence, perfect for narration.
            The value for "choices" must be a JSON array of three strings - make them generic!
            """
        full_prompt = system_prompt + "\n\nHere is the story so far:\n" + history
        response = vertex_client.models.generate_content(
            contents=full_prompt,
            model=GEMINI_MODEL
        )
        if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
            raw_text = response.candidates[0].content.parts[0].text
            logger.debug(f"Raw AI response:\n{raw_text}\n")
            json_response = raw_text.strip().replace("```json", "").replace("```", "")
            parsed = json.loads(json_response)
            logger.info("Successfully parsed story part")
            return parsed
        logger.warning("No valid response from AI model.")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}", exc_info=True)
        logger.error(f"Raw response text:\n{raw_text}\n")
        return None
    except Exception as e:
        logger.error(f"Error in get_next_story_part: {e}", exc_info=True)
        return None

def generate_audio_narration(text: str, unique_id: str, language: str = 'en') -> Optional[str]:
    # (Unchanged - includes audio cache)
    if not tts_client:
        logger.error(f"TTS client is not initialized. Error: {client_error}")
        return None
    text_hash = str(abs(hash(text)))
    if language in translated_audio_cache and text_hash in translated_audio_cache[language]:
        cached_audio_url = translated_audio_cache[language][text_hash]
        audio_path_check = os.path.join("audio", cached_audio_url.replace("/audio/", ""))
        if os.path.exists(audio_path_check):
            logger.info(f"✅ Audio cache hit for {language}: {text[:30]}...")
            return cached_audio_url
        else:
            logger.warning(f"Audio cache miss (file deleted) for {language}: {text[:30]}...")
    try:
        audio_filename = f"{language}_{unique_id}.mp3"
        audio_path = os.path.join("audio", audio_filename)
        if os.path.exists(audio_path):
             logger.info(f"Audio file already exists: {audio_path}")
             return f"/audio/{audio_filename}"
        if language == 'mr':
            lang_code = "mr-IN"
            voice_name = "mr-IN-Wavenet-B" 
            logger.info(f"Generating Marathi audio narration for text: {text[:50]}...")
        else:
            lang_code = "en-US"
            voice_name = "en-US-Neural2-C" 
            logger.info(f"Generating English audio narration for text: {text[:50]}...")
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(language_code=lang_code, name=voice_name)
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=0.95,
            pitch=2.0
        )
        response = tts_client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        with open(audio_path, "wb") as out:
            out.write(response.audio_content)
        logger.info(f"Audio saved: {audio_path}")
        audio_url = f"/audio/{audio_filename}"
        if language not in translated_audio_cache:
            translated_audio_cache[language] = {}
        translated_audio_cache[language][text_hash] = audio_url
        return audio_url
    except Exception as e:
        logger.error(f"Error generating audio: {e}", exc_info=True)
        return None

def translate_text(text: str, target_language: str, source_language: Optional[str] = None) -> str:
    # (Unchanged - This is the "smart" version from before)
    """
    Handles translation.
    - If source_language is provided, it uses it.
    - If not, it lets the API auto-detect the source.
    """
    if not translate_client:
        logger.warning("Translate client not initialized. Returning original text.")
        return text
    if not text:
        return text

    try:
        logger.debug(f"Translating: '{text[:50]}...' -> '{target_language}' (Source: {source_language or 'auto'})")
        
        if source_language:
             result = translate_client.translate(text, target_language=target_language, source_language=source_language)
        else:
             # This is used when we truly don't know the source
             result = translate_client.translate(text, target_language=target_language)
        
        translated = result['translatedText']
        logger.debug(f"Translation result: '{translated[:50]}...'")
        return translated
        
    except Exception as e:
        logger.error(f"Error during translation: {e}", exc_info=True)
        return text # Return original text on failure


def translate_story_part(story_part: Dict, target_language: str) -> Dict:
    # (Unchanged)
    if not translate_client or target_language == 'en':
        return story_part
    logger.info(f"Translating story part to {target_language}...")
    try:
        translated_part = {
            "scene_description": story_part["scene_description"], 
            # We explicitly translate from 'en' here
            "story_text": translate_text(story_part["story_text"], target_language, source_language='en'),
            "question": translate_text(story_part["question"], target_language, source_language='en'),
            "choices": [translate_text(choice, target_language, source_language='en') for choice in story_part["choices"]]
        }
        logger.info("Translation successful.")
        return translated_part
    except Exception as e:
        logger.error(f"Failed to translate story part: {e}", exc_info=True)
        return story_part

def generate_video_scene(description: str, unique_id: str) -> Optional[str]:
    # (Unchanged)
    if not vertex_client:
        logger.error(f"AI client not initialized for video. Error: {client_error}")
        raise ConnectionError(f"AI client not initialized. Error: {client_error}")
    video_filename = f"{unique_id}.mp4"
    video_path = os.path.join("videos", video_filename)
    if os.path.exists(video_path):
        logger.info(f"✅ Video file already exists (shared cache): {video_path}")
        return f"/videos/{video_filename}"
    prompt = description + ", in a bright, fun, simple 3D animated cartoon style for children, vibrant colors."
    try:
        logger.info(f"Starting video generation for prompt: {prompt[:100]}...")
        video_config = GenerateVideosConfig(aspect_ratio='16:9')
        operation = vertex_client.models.generate_videos(
            model=VEO_MODEL,
            prompt=prompt,
            config=video_config
        )
        logger.info("Video job started. Polling for completion...")
        max_wait = 300
        poll_interval = 10
        for i in range(0, max_wait, poll_interval):
            time.sleep(poll_interval)
            refreshed_op = vertex_client.operations.get(operation)
            logger.debug(f"     Polling... {i+poll_interval}s elapsed")
            if refreshed_op.done:
                operation = refreshed_op
                break
        if not operation.done:
            logger.error(f"Video generation timeout after {max_wait}s")
            return None
        logger.info("Video operation completed!")
        if operation.error:
            logger.error(f"Video generation failed with error: {operation.error}")
            return None
        if operation.result and operation.result.generated_videos:
            generated_video = operation.result.generated_videos[0]
            video_bytes = getattr(generated_video.video, 'video_bytes', None)
            if video_bytes:
                with open(video_path, "wb") as f:
                    f.write(video_bytes)
                logger.info(f"Video saved: {video_path}")
                return f"/videos/{video_filename}"
        logger.warning("No video generated - check operation result")
        return None
    except Exception as e:
        logger.error(f"Error in generate_video_scene: {e}", exc_info=True)
        return None

def find_best_matching_cache_key(target_key: str) -> Optional[str]:
    # (Unchanged)
    target_words = set(target_key.split())
    with cache_lock:
        if target_key in api_content_cache:
            logger.info(f"     ✅ Exact cache match found: '{target_key[:50]}...'")
            return target_key
        best_match = None
        best_match_score = 0
        for cache_key in api_content_cache.keys():
            cache_words = set(cache_key.split())
            matching_words = target_words.intersection(cache_words)
            match_score = len(matching_words)
            if matching_words == target_words and match_score > best_match_score:
                best_match = cache_key
                best_match_score = match_score
                logger.info(f"     🔍 Found partial match: '{cache_key[:50]}...' (score: {match_score})")
    if best_match:
        logger.info(f"     ✅ Best matching cache key: '{best_match[:50]}...'")
        return best_match
    return None

def get_or_create_english_scene(
    story_context_en: str,
    use_last_scene_only: bool = False, 
    is_first_scene: bool = False,
):
    # (Unchanged - EN only logic)
    if use_last_scene_only and "\n" in story_context_en:
        context_lines = story_context_en.strip().split("\n")
        initial_idea_line = context_lines[0]
        if "The story starts with:" in initial_idea_line:
            initial_idea = initial_idea_line.split("The story starts with:")[-1].strip()
        else:
            initial_idea = initial_idea_line
        last_line = context_lines[-1] if context_lines else story_context_en
        if "chose that they should:" in last_line:
            choice = last_line.split("chose that they should:")[-1].strip()
        else:
            choice = last_line
        search_context_en = f"{initial_idea} {choice}"
    else:
        search_context_en = story_context_en
    logger.info(f"🔍 English Context: '{search_context_en[:100]}...'")
    canonical_key_str = normalize_prompt_for_cache(search_context_en)
    logger.info(f"     English Cache Key: '{canonical_key_str[:100]}...'")
    video_canonical_key = PROMPT_TO_VIDEO_KEY_MAP.get(canonical_key_str)
    if not video_canonical_key:
        logger.warning(f"     Prompt not in shared map. Using EN key as video key.")
        video_canonical_key = canonical_key_str
    video_file_id = str(abs(hash(video_canonical_key)))
    logger.info(f"     Shared Video Key: '{video_canonical_key[:100]}...' (ID: {video_file_id})")
    matching_cache_key = find_best_matching_cache_key(canonical_key_str)
    if matching_cache_key:
        with cache_lock:
             cached_data = api_content_cache.get(matching_cache_key)
        if cached_data:
            logger.info("✅✅✅ ENGLISH CACHE HIT! Returning cached content instantly!")
            return cached_data
    logger.info(f"❌ CACHE MISS. Proceeding with new content generation for: '{canonical_key_str[:50]}...'")
    with cache_lock:
        if find_best_matching_cache_key(canonical_key_str):
             logger.info("✅✅✅ CACHE HIT! (Another thread just finished).")
             return api_content_cache[canonical_key_str]
    story_part = get_next_story_part(story_context_en, is_first_scene=is_first_scene)
    if not story_part:
        raise ValueError("Failed to generate story part from API.")
    scene_description = story_part["scene_description"]
    logger.info("🔄 Generating video (or finding shared file)...")
    video_url = generate_video_scene(scene_description, video_file_id)
    if not video_url:
        logger.error(f"❌ VIDEO GENERATION FAILED for prompt: {scene_description}")
        raise ValueError("Failed to generate video scene. Check app.log.")
    logger.info("🔄 Generating ENGLISH audio narration...")
    audio_file_id = abs(hash(story_part["story_text"]))
    audio_url = generate_audio_narration(story_part["story_text"], str(audio_file_id), language='en')
    scene_data = {
        "story_part": story_part,
        "video_url": video_url,
        "audio_url": audio_url
    }
    logger.info("✅ New English content generated!")
    with cache_lock:
        api_content_cache[canonical_key_str] = scene_data
    return scene_data


# ======================================================================================
# API ENDPOINTS
# ======================================================================================
@app.get("/videos/{filename}")
async def get_video(filename: str):
    video_path = os.path.join("videos", filename)
    if not os.path.exists(video_path):
        logger.error(f"File not found: {video_path}")
        raise HTTPException(status_code=404, detail="Video file not found")
    return FileResponse(video_path, media_type="video/mp4")

@app.get("/audio/{filename}")
async def get_audio(filename: str):
    audio_path = os.path.join("audio", filename)
    if not os.path.exists(audio_path):
        logger.error(f"File not found: {audio_path}")
        raise HTTPException(status_code=404, detail="Audio file not found")
    return FileResponse(audio_path, media_type="audio/mpeg")


@app.get("/")
async def root():
    return {"message": "AI Cartoon Story Builder API with TTS (Unlimited Cache)", "status": "running"}

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "ai_client_initialized": vertex_client is not None,
        "tts_client_initialized": tts_client is not None,
        "translate_client_initialized": translate_client is not None,
        "speech_client_initialized": speech_client is not None, # <-- Added
        "client_error": client_error,
        "active_sessions": len(story_sessions),
        "cache_size": len(api_content_cache),
        "cache_mode": "unlimited"
    }

# --- BLOCK 2: UPDATED API endpoint for live translation ---
@app.post("/api/translate")
async def api_translate(request: TranslateRequest):
    if not translate_client:
        raise HTTPException(status_code=500, detail="Translation client not initialized.")
    if not request.text.strip():
        return {"translated_text": ""}
    
    try:
        # --- THIS IS THE FIX ---
        # We *force* the source language to be 'en' for this specific feature.
        # This assumes the user is typing in English to have it auto-translated.
        source_lang = 'en'
        
        # However, if the target is 'en', we auto-detect the source.
        if request.target_lang == 'en':
            source_lang = None 
        
        translated_text = await run_in_threadpool(
            translate_text,
            request.text,
            request.target_lang,
            source_language=source_lang 
        )
        return {"translated_text": translated_text}
    except Exception as e:
        logger.error(f"Error in /api/translate: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Translation failed: {e}")
# --- END OF BLOCK 2 ---


# === NEW: /api/transcribe ENDPOINT ===
@app.post("/api/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    language: str = Form("en-US") # e.g., 'en-US' or 'mr-IN'
):
    if not speech_client:
        logger.error("Speech client not initialized.")
        raise HTTPException(status_code=500, detail="Speech client not initialized.")

    try:
        logger.info(f"Receiving audio file for transcription in {language}...")
        
        # Read audio content
        content = await file.read()

        # Configure the audio and request
        audio = speech.RecognitionAudio(content=content)
        
        # The frontend will send 'audio/webm;codecs=opus'
        # Google STT supports this with the WEBM_OPUS encoding
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
            language_code=language,
            # sample_rate_hertz is not needed for WEBM_OPUS
        )

        logger.info(f"Sending audio to Google STT API ({language})...")
        # Perform transcription
        response = await run_in_threadpool(speech_client.recognize, config=config, audio=audio)
        
        if response.results and response.results[0].alternatives:
            transcript = response.results[0].alternatives[0].transcript
            logger.info(f"Transcription successful: {transcript}")
            return {"transcript": transcript}
        else:
            logger.warning("Transcription returned no results.")
            return {"transcript": ""}

    except Exception as e:
        logger.error(f"Error in /api/transcribe: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Transcription failed: {e}")
# === END OF NEW ===


@app.post("/api/start-story")
async def start_story(request: StartStoryRequest, background_tasks: BackgroundTasks):
    # (Unchanged)
    logger.info(f"🚀 START STORY REQUEST: '{request.initial_idea}' in lang '{request.language}'")
    if not vertex_client:
        raise HTTPException(status_code=500, detail=f"AI client not initialized. Error: {client_error}")
    try:
        session_id = f"session_{int(time.time())}"
        initial_idea_text_en = request.initial_idea.strip()
        if request.language != 'en':
            # Translate to 'en', let API auto-detect source
            initial_idea_text_en = await run_in_threadpool(translate_text, initial_idea_text_en, 'en', source_language=None)
            logger.info(f"     Translated initial idea to EN: '{initial_idea_text_en}'")
        if not initial_idea_text_en:
             raise HTTPException(status_code=400, detail="Initial idea cannot be empty.")
        corrected_context = correct_spelling(initial_idea_text_en)
        if corrected_context:
            initial_idea_text_en = corrected_context
        start_time = time.time()
        scene_data_en = await run_in_threadpool(
            get_or_create_english_scene,
            story_context_en=initial_idea_text_en,
            use_last_scene_only=False, 
            is_first_scene=True
        )
        background_tasks.add_task(save_cache_to_disk, api_content_cache)
        final_story_part = scene_data_en["story_part"]
        video_url = scene_data_en["video_url"]
        audio_url = scene_data_en["audio_url"]
        if request.language != 'en':
            logger.info(f"     Translating story part to {request.language}...")
            final_story_part = await run_in_threadpool(
                translate_story_part,
                scene_data_en["story_part"],
                request.language
            )
            logger.info(f"     Generating {request.language} audio...")
            audio_file_id = abs(hash(final_story_part["story_text"]))
            audio_url = await run_in_threadpool(
                generate_audio_narration,
                final_story_part["story_text"], 
                str(audio_file_id), 
                request.language
            )
        elapsed_time = time.time() - start_time
        logger.info(f"⏱️ Request completed in {elapsed_time:.2f} seconds")
        story_sessions[session_id] = {
            "history_en": [f"The story starts with: {initial_idea_text_en}"],
            "current_part_en": scene_data_en["story_part"]
        }
        return {
            "session_id": session_id,
            "story_part": final_story_part,
            "video_url": video_url,
            "audio_url": audio_url
        }
    except Exception as e:
        logger.error(f"❌ Unexpected error in start_story: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to start story. {e}")


@app.post("/api/continue-story")
async def continue_story(request: ContinueStoryRequest, background_tasks: BackgroundTasks):
    # (Unchanged)
    logger.info(f"➡️ CONTINUE STORY REQUEST for session {request.session_id} in lang '{request.language}'")
    session = story_sessions.get(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Active story session not found.")
    try:
        choice_text_en = request.choice
        if request.language != 'en':
            translated_choices = [
                await run_in_threadpool(translate_text, c, request.language, source_language='en') 
                for c in session["current_part_en"]["choices"]
            ]
            try:
                choice_index = translated_choices.index(request.choice)
                choice_text_en = session["current_part_en"]["choices"][choice_index]
                logger.info(f"     Mapped choice '{request.choice}' to EN '{choice_text_en}'")
            except ValueError:
                logger.warning(f"     Could not map choice '{request.choice}'. Translating back to EN.")
                choice_text_en = await run_in_threadpool(translate_text, request.choice, 'en', source_language=None)
        session["history_en"].append(f"Then, the child chose that they should: {choice_text_en}")
        story_context_en = "\n".join(session["history_en"])
        start_time = time.time()
        scene_data_en = await run_in_threadpool(
            get_or_create_english_scene,
            story_context_en=story_context_en,
            use_last_scene_only=True, 
            is_first_scene=False
        )
        background_tasks.add_task(save_cache_to_disk, api_content_cache)
        final_story_part = scene_data_en["story_part"]
        video_url = scene_data_en["video_url"]
        audio_url = scene_data_en["audio_url"]
        if request.language != 'en':
            logger.info(f"     Translating story part to {request.language}...")
            final_story_part = await run_in_threadpool(
                translate_story_part,
                scene_data_en["story_part"],
                request.language
            )
            logger.info(f"     Generating {request.language} audio...")
            audio_file_id = abs(hash(final_story_part["story_text"]))
            audio_url = await run_in_threadpool(
                generate_audio_narration,
                final_story_part["story_text"], 
                str(audio_file_id), 
                request.language
            )
        elapsed_time = time.time() - start_time
        logger.info(f"⏱️ Request completed in {elapsed_time:.2f} seconds")
        session["current_part_en"] = scene_data_en["story_part"]
        return {
            "story_part": final_story_part,
            "video_url": video_url,
            "audio_url": audio_url
        }
    except Exception as e:
        logger.error(f"❌ Unexpected error in continue_story: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to continue story. {e}")


@app.post("/api/reset")
async def reset_story(request: ResetStoryRequest):
    # (Unchanged)
    if request.session_id and request.session_id in story_sessions:
        del story_sessions[request.session_id]
        logger.info(f"🔄 Story session reset: {request.session_id}")
        return {"message": f"Story session {request.session_id} reset successfully"}
    if not request.session_id:
        logger.info("🔄 All story sessions reset")
        story_sessions.clear()
        return {"message": "All stories reset successfully"}
    logger.info("No active session to reset")
    return {"message": "No active session to reset"}


# ======================================================================================
# RUN SERVER
# ======================================================================================
# --- This block is commented out as requested ---
# if __name__ == "__main__":
#     import uvicorn
#     logger.info(f"\n{'='*60}")
#     logger.info(f"🚀 Starting AI Cartoon Story Builder API with TTS (Unlimited Cache)")
#     logger.info(f"     Host: {SERVER_HOST}")
#     logger.info(f"     Port: {SERVER_PORT}")
#     logger.info(f"{'='*60}\n")
    
#     # Remember to use log_config=None to see your custom logs!
#     uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT, log_config=None)
