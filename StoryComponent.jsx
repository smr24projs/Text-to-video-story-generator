// import React, { useState, useRef, useEffect } from 'react';

// // (Imports and translations remain the same)
// const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

// const translations = {
//   en: {
//     title: "AI Story Builder",
//     subtitle: "Synced video & narration! 🎬🎙️",
//     errorPrefix: "Oops!",
//     startTitle: "Let's start a new adventure!",
//     placeholder: "e.g., A brave knight and a funny dragon",
//     suggestionHeader: "Or try one of these ideas:",
//     suggestions: [
//       "sun with the moon",
//       "a brave knight and friendly dragon",
//       "a little girl and bear"
//     ],
//     startStory: "Start My Story! 🚀",
//     loadingStart: "Creating your story...",
//     loadingScene: "Creating your magical scene...",
//     loadingSceneSub: "Generating synced video and narration ✨",
//     videoLoading: "Video is loading...",
//     titlePause: "Pause",
//     titlePlay: "Play",
//     titleMute: "Mute video",
//     titleUnmute: "Unmute video",
//     replay: "Replay",
//     titleFullscreenEnter: "Enter Fullscreen",
//     titleFullscreenExit: "Exit Fullscreen",
//     titleSubtitlesOn: "Hide Subtitles",
//     titleSubtitlesOff: "Show Subtitles",
//     narratorLabel: "Narrator:",
//     narrating: "Narrating...",
//     thinking: "Thinking...",
//     loadingNextScene: "Creating the next scene with narration...",
//     reset: "Start a New Story"
//   },
//   mr: {
//     title: "AI कथा निर्माता",
//     subtitle: "सिंक केलेला व्हिडिओ आणि निवेदन! 🎬🎙️",
//     errorPrefix: "अरे!",
//     startTitle: "चला एक नवीन साहस सुरू करूया!",
//     placeholder: "उदा. एक शूर योद्धा आणि एक मजेदार ड्रॅगन",
//     suggestionHeader: "किंवा यापैकी एक कल्पना वापरून पहा:",
//     suggestions: [
//       "सूर्य आणि चंद्र",
//       "एक शूर योद्धा आणि एक मित्र ड्रॅगन",
//       "एक लहान मुलगी आणि अस्वल"
//     ],
//     startStory: "माझी कथा सुरू करा! 🚀",
//     loadingStart: "तुमची कथा तयार करत आहे...",
//     loadingScene: "तुमचे जादुई दृश्य तयार करत आहे...",
//     loadingSceneSub: "सिंक केलेला व्हिडिओ आणि निवेदन तयार होत आहे ✨",
//     videoLoading: "व्हिडिओ लोड होत आहे...",
//     titlePause: "विराम",
//     titlePlay: "प्ले",
//     titleMute: "व्हिडिओ म्यूट करा",
//     titleUnmute: "व्हिडिओ अनम्यूट करा",
//     replay: "पुन्हा प्ले करा",
//     titleFullscreenEnter: "पूर्णस्क्रीन",
//     titleFullscreenExit: "पूर्णस्क्रीनमधून बाहेर पडा",
//     titleSubtitlesOn: "उपशीर्षके लपवा",
//     titleSubtitlesOff: "उपशीर्षके दर्शवा",
//     narratorLabel: "निवेदक:",
//     narrating: "निवेदन करत आहे...",
//     thinking: "विचार करत आहे...",
//     loadingNextScene: "पुढील दृश्य निवेदनासह तयार करत आहे...",
//     reset: "नवीन कथा सुरू करा"
//   }
// };

// const enToMrSuggestionsMap = {
//   "sun with the moon": "सूर्य आणि चंद्र",
//   "a brave knight and friendly dragon": "एक शूर योद्धा आणि एक मित्र ड्रॅगन",
//   "a tortoise and rabbit": "कासव आणि ससा",
//   "a little girl and bear": "एक लहान मुलगी आणि अस्वल",
//   "the monkey and the crocodile": "माकड आणि मगर",
//   "stork and crab": "सारस आणि खेकडा"
// };

// // (All Icon components remain the same...)
// const SparklesIcon = () => (
//   <svg className="w-10 h-10" fill="currentColor" viewBox="0 0 24 24">
//     <path d="M12 0l1.545 5.633L19 7.5l-5.455 1.867L12 15l-1.545-5.633L5 7.5l5.455-1.867L12 0zM4 12l1.029 3.756L9 17l-3.971 1.244L4 22l-1.029-3.756L0 17l3.971-1.244L4 12zm16 0l1.029 3.756L25 17l-3.971 1.244L20 22l-1.029-3.756L16 17l3.971-1.244L20 12z"/>
//   </svg>
// );
// const VideoIcon = () => (
//   <svg className="w-16 h-16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
//     <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
//   </svg>
// );
// const LoaderIcon = ({ className = "h-12 w-12" }) => (
//   <svg className={`animate-spin ${className}`} fill="none" viewBox="0 0 24 24">
//     <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
//     <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
//   </svg>
// );
// const ResetIcon = () => (
//   <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
//     <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
//   </svg>
// );
// const VolumeIcon = () => (
//   <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
//     <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
//   </svg>
// );
// const VolumeMuteIcon = () => (
//   <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
//     <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z M17 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2" />
//   </svg>
// );
// const PlayIcon = () => (
//   <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
//     <path d="M8 5v14l11-7z" />
//   </svg>
// );
// const PauseIcon = () => (
//   <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
//     <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z" />
//   </svg>
// );
// const FullscreenEnterIcon = () => (
//   <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
//     <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 8V4h4m12 4V4h-4M4 16v4h4m12-4v4h-4" />
//   </svg>
// );
// const FullscreenExitIcon = () => (
//   <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
//     <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 4H4v4m12-4h4v4M8 20H4v-4m12 4h4v-4" />
//   </svg>
// );
// const CCIcon = () => (
//     <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
//         <path d="M20 4H4C2.9 4 2 4.9 2 6v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zM9.5 15c0 .83-.67 1.5-1.5 1.5H6.5c-.83 0-1.5-.67-1.5-1.5v-3c0-.83.67-1.5 1.5-1.5h1.5c.83 0 1.5.67 1.5 1.5v3zm7 0c0 .83-.67 1.5-1.5 1.5h-1.5c-.83 0-1.5-.67-1.5-1.5v-3c0-.83.67-1.5 1.5-1.5h1.5c.83 0 1.5.67 1.5 1.5v3z"/>
//     </svg>
// );
// const CCOffIcon = () => (
//     <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
//         <path d="M2.81 2.81L1.39 4.22L3 5.83V18c0 1.1.9 2 2 2h12.17l2.61 2.61l1.41-1.41L2.81 2.81zM5 18V7.83l10.17 10.17H5zm15-1.17L10.83 8H16.5c.83 0 1.5.67 1.5 1.5v3c0 .83-.67 1.5-1.5 1.5h-1.5v-1.5h1.5v-3H15v1.17l-3-3V9c0-.83.67-1.5 1.5-1.5h1.5c.83 0 1.5.67 1.5 1.5v.17l4.78 4.78C20 13.65 20 13.34 20 13v-3c0-1.1-.9-2-2-2H9.83l-4-4H20c1.1 0 2 .9 2 2v12c0 .35-.09.68-.24.97l-1.6-1.6C19.9 17.54 20 17.77 20 18v-4.17zM9.5 15c0 .83-.67 1.5-1.5 1.5H6.5c-.83 0-1.5-.67-1.5-1.5v-3c0-.83.67-1.5 1.5-1.5h1.5c.83 0 1.5.67 1.5 1.5v3z"/>
//     </svg>
// );


// const formatTime = (timeInSeconds) => {
//   if (isNaN(timeInSeconds) || timeInSeconds === 0) return "0:00";
//   const minutes = Math.floor(timeInSeconds / 60);
//   const seconds = Math.floor(timeInSeconds % 60);
//   return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
// };

// export default function CartoonStoryBuilder() {
//   const [storyState, setStoryState] = useState('initial');
//   const [initialIdea, setInitialIdea] = useState('');
//   const [currentScene, setCurrentScene] = useState(null);
//   const [videoUrl, setVideoUrl] = useState(null);
//   const [audioUrl, setAudioUrl] = useState(null);
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState(null);
//   const [sessionId, setSessionId] = useState(null);
//   const [isNarrating, setIsNarrating] = useState(false);
//   const [videoVolume, setVideoVolume] = useState(0.1);
//   const [isVideoReady, setIsVideoReady] = useState(false);
//   const [isAudioReady, setIsAudioReady] = useState(false);
//   const [isPlaying, setIsPlaying] = useState(false);
//   const [isFullscreen, setIsFullscreen] = useState(false);
//   const [language, setLanguage] = useState('en');
//   const [duration, setDuration] = useState(0);
//   const [currentTime, setCurrentTime] = useState(0);
//   const [buffered, setBuffered] = useState(0);
//   const [showSubtitles, setShowSubtitles] = useState(true);
//   const t = translations[language]; 
//   const [subtitleWords, setSubtitleWords] = useState([]);
//   const [visibleSubtitle, setVisibleSubtitle] = useState('');
//   const [debouncedIdea, setDebouncedIdea] = useState(initialIdea);
//   const [isTranslating, setIsTranslating] = useState(false);
//   const isMounted = useRef(false); 
//   const audioRef = useRef(null);
//   const videoRef = useRef(null);
//   const playerContainerRef = useRef(null);

//   // (All useEffects and handler functions remain the same...)
//   useEffect(() => {
//     const onFullscreenChange = () => {
//       setIsFullscreen(!!document.fullscreenElement);
//     };
//     document.addEventListener('fullscreenchange', onFullscreenChange);
//     return () => document.removeEventListener('fullscreenchange', onFullscreenChange);
//   }, []);

//   useEffect(() => {
//     if (videoUrl) {
//       setIsVideoReady(false);
//       setIsAudioReady(false); 
//       setCurrentTime(0);
//       setDuration(0);
//       setBuffered(0);
//       if (videoRef.current) {
//         videoRef.current.pause();
//         videoRef.current.currentTime = 0;
//       }
//       if (audioRef.current) {
//         audioRef.current.pause();
//         audioRef.current.currentTime = 0;
//       }
//       if (!audioUrl) {
//         setIsAudioReady(true);
//       }
//     }
//   }, [audioUrl, videoUrl]);

//   useEffect(() => {
//     const canPlay = isVideoReady && (isAudioReady || !audioUrl) && videoRef.current;
//     if (canPlay) {
//       const playMedia = async () => {
//         try {
//           videoRef.current.volume = videoVolume;
//           if (audioRef.current) {
//             await Promise.all([
//               videoRef.current.play(),
//               audioRef.current.play()
//             ]);
//           } else {
//             await videoRef.current.play();
//           }
//         } catch (error) {
//           console.error('Error starting playback:', error);
//         }
//       };
//       playMedia();
//     }
//   }, [isVideoReady, isAudioReady, videoVolume, audioUrl]);

//   useEffect(() => {
//     if (currentScene?.story_text) {
//       setSubtitleWords(currentScene.story_text.split(' '));
//       setVisibleSubtitle(''); // Reset on new scene
//     } else {
//       setSubtitleWords([]);
//       setVisibleSubtitle('');
//     }
//   }, [currentScene]);

//   useEffect(() => {
//     const handler = setTimeout(() => {
//       setDebouncedIdea(initialIdea);
//     }, 1200);

//     return () => {
//       clearTimeout(handler);
//     };
//   }, [initialIdea]);

//   useEffect(() => {
//     if (!isMounted.current) {
//       isMounted.current = true;
//       return;
//     }
//     const translateIdea = async () => {
//       if (language === 'mr' && debouncedIdea.trim()) {
//         const hardcodedTranslation = enToMrSuggestionsMap[debouncedIdea.trim().toLowerCase()];
//         if (hardcodedTranslation) {
//           if (hardcodedTranslation !== initialIdea) {
//             setInitialIdea(hardcodedTranslation);
//           }
//           return; 
//         }
//         setIsTranslating(true);
//         try {
//           const response = await fetch(`${API_BASE_URL}/api/translate`, {
//             method: 'POST',
//             headers: { 'Content-Type': 'application/json' },
//             body: JSON.stringify({ text: debouncedIdea, target_lang: 'mr' })
//           });
//           if (!response.ok) {
//             const errData = await response.json().catch(() => ({}));
//             throw new Error(errData.detail || 'Translation service failed');
//           }
//           const data = await response.json();
//           if (data.translated_text && data.translated_text !== initialIdea) {
//             setInitialIdea(data.translated_text);
//           }
//         } catch (err) {
//           console.error("Translation error:", err.message);
//         } finally {
//           setIsTranslating(false);
//         }
//       }
//     };
//     translateIdea();
//   }, [debouncedIdea, language]);

//   const handlePlaybackChange = (playing) => {
//     setIsNarrating(playing);
//     setIsPlaying(playing);
//   };
//   const togglePlayPause = () => {
//     if (!videoRef.current) return;
//     if (isPlaying) {
//       videoRef.current.pause();
//       if (audioRef.current) {
//         audioRef.current.pause();
//       }
//     } else {
//       videoRef.current.play();
//       if (audioRef.current) {
//         audioRef.current.play();
//       }
//     }
//   };
//   const toggleVideoVolume = () => {
//     const newVolume = videoVolume > 0 ? 0 : 0.1;
//     setVideoVolume(newVolume);
//     if (videoRef.current) {
//       videoRef.current.volume = newVolume;
//     }
//   };
//   const replayScene = () => {
//     if (videoRef.current) {
//       setIsVideoReady(false);
//       setIsAudioReady(false);
//       setCurrentTime(0);
//       setVisibleSubtitle(''); // Reset visible words
//       videoRef.current.currentTime = 0;
//       if (audioRef.current) {
//         audioRef.current.currentTime = 0;
//       }
//       if (!audioUrl) {
//         setIsAudioReady(true);
//       }
//     }
//   };
//   const toggleFullscreen = () => {
//     if (!document.fullscreenElement) {
//       playerContainerRef.current?.requestFullscreen().catch(err => {
//         alert(`Error attempting to enable full-screen mode: ${err.message} (${err.name})`);
//       });
//     } else {
//       document.exitFullscreen();
//     }
//   };
//   const handleSeek = (e) => {
//     if (!videoRef.current || isNaN(duration) || duration === 0) return;
//     const progressBar = e.currentTarget;
//     const clickPosition = e.nativeEvent.offsetX;
//     const barWidth = progressBar.clientWidth;
//     const seekTime = (clickPosition / barWidth) * duration;
//     videoRef.current.currentTime = seekTime;
//     if(audioRef.current) {
//       audioRef.current.currentTime = seekTime;
//     }
//     setCurrentTime(seekTime);
//   };
//   const executeStartStory = async (prompt) => {
//     if (!prompt.trim()) return;
//     setLoading(true);
//     setError(null);
//     setStoryState('loading');
//     try {
//       const response = await fetch(`${API_BASE_URL}/api/start-story`, {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({ 
//           initial_idea: prompt,
//           language: language
//         })
//       });
//       if (!response.ok) {
//         const errorData = await response.json().catch(() => ({}));
//         throw new Error(errorData.detail || `Failed to start story`);
//       }
//       const data = await response.json();
//       setSessionId(data.session_id);
//       setCurrentScene(data.story_part);
//       setVideoUrl(data.video_url);
//       setAudioUrl(data.audio_url);
//       setStoryState('scene');
//     } catch (err) {
//       setError(err.message);
//       setStoryState('initial');
//     } finally {
//       setLoading(false);
//     }
//   };
//   const startStory = async () => {
//     executeStartStory(initialIdea);
//   };
//   const handleSuggestionClick = (suggestion) => {
//     setInitialIdea(suggestion); 
//     executeStartStory(suggestion); 
//   };
//   const makeChoice = async (choice) => {
//     setLoading(true);
//     setError(null);
//     try {
//       const response = await fetch(`${API_BASE_URL}/api/continue-story`, {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({ 
//           session_id: sessionId, 
//           choice: choice,
//           language: language
//         })
//       });
//       if (!response.ok) {
//         const errorData = await response.json().catch(() => ({}));
//         throw new Error(errorData.detail || `Failed to continue story`);
//       }
//       const data = await response.json();
//       setCurrentScene(data.story_part);
//       setVideoUrl(data.video_url);
//       setAudioUrl(data.audio_url);
//     } catch (err) {
//       setError(err.message);
//     } finally {
//       setLoading(false);
//     }
//   };
//   const handleFullReset = async () => {
//      try {
//       await fetch(`${API_BASE_URL}/api/reset`, { 
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({ session_id: null }) // Resets *all* sessions
//       });
//       alert('All story sessions have been reset!');
//     } catch (err) {
//       console.error('Full reset failed:', err);
//       alert('Could not reset sessions.');
//     }
//   };

//   return (
//     <div className="min-h-screen bg-gradient-to-br from-purple-100 via-pink-100 to-blue-100 p-4 font-sans">
//       <div className="max-w-6xl mx-auto">
        
//         <div className="text-center mb-8 pt-8">
//           <h1 className="text-5xl font-bold text-purple-600 mb-2 flex items-center justify-center gap-3">
//             <SparklesIcon />
//             {t.title} 
//             <SparklesIcon />
//           </h1>
//           <p className="text-gray-600 text-lg">{t.subtitle}</p>
//         </div>

//         {audioUrl && (
//           <audio
//             ref={audioRef}
//             src={`${API_BASE_URL}${audioUrl}`}
//             onCanPlayThrough={() => setIsAudioReady(true)}
//             onPlay={() => handlePlaybackChange(true)}
//             onEnded={() => handlePlaybackChange(false)}
//             onPause={() => handlePlaybackChange(false)}
//           />
//         )}


//         {error && (
//           <div className="bg-red-100 border-2 border-red-400 rounded-lg p-4 mb-6">
//             <p className="text-red-700 font-semibold">{t.errorPrefix}! {error}</p>
//           </div>
//         )}

//         {storyState === 'initial' && (
//           <div className="bg-white rounded-2xl shadow-xl p-8 mb-6">
            
//             <div className="flex justify-between items-center mb-4">
//                 <h2 className="text-2xl font-bold text-gray-800">
//                   {t.startTitle}
//                 </h2>
//                 <select 
//                   value={language} 
//                   onChange={(e) => setLanguage(e.target.value)}
//                   className="bg-white border-2 border-purple-300 rounded-lg px-3 py-2 text-purple-700 font-medium focus:outline-none focus:border-purple-500"
//                 >
//                   <option value="en">English</option>
//                   <option value="mr">मराठी (Marathi)</option>
//                 </select>
//             </div>

//             <div className="relative">
//               <input
//                 type="text"
//                 value={initialIdea}
//                 onChange={(e) => setInitialIdea(e.target.value)}
//                 placeholder={t.placeholder}
//                 className="w-full px-4 py-3 border-2 border-purple-300 rounded-lg mb-4 text-lg focus:outline-none focus:border-purple-500"
//                 onKeyPress={(e) => e.key === 'Enter' && startStory()}
//               />
//               {isTranslating && (
//                 <div className="absolute right-4 top-1/2 -translate-y-1/2" style={{top: '1.1rem'}}>
//                   <LoaderIcon className="h-5 w-5 text-purple-400" />
//                 </div>
//               )}
//             </div>


//             <div className="my-4">
//               <p className="text-base text-gray-500 mb-2 text-center">{t.suggestionHeader}</p>
//               <div className="flex flex-wrap justify-center gap-2">
//                 {t.suggestions.map((suggestion) => (
//                   <button
//                     key={suggestion}
//                     onClick={() => handleSuggestionClick(suggestion)}
//                     disabled={loading}
//                     className="px-6 py-3 bg-purple-50 hover:bg-purple-100 text-purple-600 font-medium rounded-full text-base transition-all disabled:opacity-50 disabled:cursor-not-allowed"
//                   >
//                     {suggestion}
//                   </button>
//                 ))}
//               </div>
//             </div>
            
//             <button
//               onClick={startStory}
//               disabled={!initialIdea.trim() || loading || isTranslating}
//               className="w-full bg-gradient-to-r from-purple-500 to-pink-500 text-white font-bold py-3 rounded-lg text-lg hover:from-purple-600 hover:to-pink-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:scale-105 mt-4"
//             >
//               {loading ? t.loadingStart : (isTranslating ? 'Translating...' : t.startStory)}
//             </button>
            
//           </div>
//         )}

        
//         {storyState === 'loading' && (
//           <div className="bg-white rounded-2xl shadow-xl p-12 text-center">
//             <div className="text-purple-500 flex justify-center mb-4">
//               <LoaderIcon className="h-12 w-12" />
//             </div>
//             <h3 className="text-2xl font-bold text-gray-800 mb-2">
//               {t.loadingScene}
//             </h3>
//             <p className="text-gray-600">{t.loadingSceneSub}</p>
//           </div>
//         )}

//         {storyState === 'scene' && currentScene && (
//           <div className="space-y-6">

//             <div className="space-y-6">
            
//               {/* --- THIS IS THE UPDATED LINE --- */}
//               <div ref={playerContainerRef} className="bg-white rounded-2xl shadow-xl p-6 max-w-3xl mx-auto">
//                 {videoUrl ? (
//                   <div className="relative">
//                     <video
//                       ref={videoRef}
//                       key={videoUrl}
//                       loop
//                       playsInline
//                       className="w-full rounded-lg shadow-lg bg-black cursor-pointer"
//                       src={`${API_BASE_URL}${videoUrl}`}
//                       onCanPlayThrough={() => setIsVideoReady(true)}
//                       onClick={togglePlayPause}
//                       onLoadedMetadata={() => setDuration(videoRef.current.duration)}
//                       onTimeUpdate={() => {
//                         if (!videoRef.current) return;
//                         const time = videoRef.current.currentTime;
//                         setCurrentTime(time);
//                         if (videoRef.current.buffered.length > 0) {
//                           setBuffered(videoRef.current.buffered.end(videoRef.current.buffered.length - 1));
//                         }
//                         if (duration > 0 && subtitleWords.length > 0) {
//                           const timePerWord = duration / subtitleWords.length;
//                           const wordCountToShow = Math.floor(time / timePerWord) + 1;
//                           const visibleWords = subtitleWords.slice(0, wordCountToShow).join(' ');
//                           setVisibleSubtitle(visibleWords);
//                         }
//                       }}
//                     />
                    
//                     {showSubtitles && currentScene && (
//                       <div 
//                         className="absolute bottom-16 md:bottom-20 left-1/2 -translate-x-1/2 w-full px-4 pointer-events-none"
//                       >
//                         <p 
//                           className="text-center text-lg md:text-2xl font-semibold text-white"
//                           style={{ textShadow: '2px 2px 4px rgba(0, 0, 0, 0.8)' }} 
//                         >
//                           {visibleSubtitle}
//                         </p>
//                       </div>
//                     )}
                    
//                     <div className="absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-black/60 to-transparent">
//                       <div 
//                         className="relative w-full h-1.5 bg-white/20 rounded-full cursor-pointer"
//                         onClick={handleSeek}
//                       >
//                         <div 
//                           className="absolute left-0 top-0 h-full bg-white/40 rounded-full" 
//                           style={{ width: `${(buffered / duration) * 100}%` }} 
//                         />
//                         <div 
//                           className="absolute left-0 top-0 h-full bg-pink-500 rounded-full" 
//                           style={{ width: `${(currentTime / duration)* 100}%` }} 
//                         />
//                       </div>
                      
//                       <div className="flex justify-between items-center mt-2 text-white">
//                         <div className="flex gap-2 items-center">
//                           <button
//                             onClick={togglePlayPause}
//                             className="bg-transparent hover:bg-black/70 text-white p-2 rounded-full transition-all"
//                             title={isPlaying ? t.titlePause : t.titlePlay}
//                           >
//                             {isPlaying ? <PauseIcon /> : <PlayIcon />}
//                           </button>
//                           <button
//                             onClick={toggleVideoVolume}
//                             className="bg-transparent hover:bg-black/70 text-white p-2 rounded-full transition-all"
//                             title={videoVolume > 0 ? t.titleMute : t.titleUnmute}
//                           >
//                             {videoVolume > 0 ? <VolumeIcon /> : <VolumeMuteIcon />}
//                           </button>
//                           <button
//                             onClick={replayScene}
//                             className="bg-transparent hover:bg-black/70 text-white px-3 py-1 text-sm rounded-full transition-all"
//                           >
//                             {t.replay}
//                           </button>
//                         </div>
                        
//                         <div className="text-sm font-medium">
//                           {formatTime(currentTime)} / {formatTime(duration)}
//                         </div>
                        
//                         <div className="flex gap-2 items-center">
//                           <button
//                             onClick={() => setShowSubtitles(!showSubtitles)}
//                             className={`bg-transparent hover:bg-black/70 p-2 rounded-full transition-all ${
//                               showSubtitles ? 'text-pink-400' : 'text-white'
//                             }`}
//                             title={showSubtitles ? t.titleSubtitlesOn : t.titleSubtitlesOff}
//                           >
//                             {showSubtitles ? <CCIcon /> : <CCOffIcon />}
//                           </button>
//                           <button
//                             onClick={toggleFullscreen}
//                             className="bg-transparent hover:bg-black/70 text-white p-2 rounded-full transition-all"
//                             title={isFullscreen ? t.titleFullscreenExit : t.titleFullscreenEnter}
//                           >
//                             {isFullscreen ? <FullscreenExitIcon /> : <FullscreenEnterIcon />}
//                           </button>
//                         </div>
//                       </div>
//                     </div>
//                   </div>
//                 ) : (
//                   <div className="bg-gray-100 rounded-lg p-12 text-center">
//                     <div className="text-gray-400 flex justify-center mb-4">
//                       <VideoIcon />
//                     </div>
//                     <p className="text-gray-600">{t.videoLoading}</p>
//                   </div>
//                 )}
//               </div>

//               {/* --- THIS IS THE UPDATED LINE --- */}
//               <div className="bg-white rounded-2xl shadow-xl p-6 max-w-3xl mx-auto">
//                 <h3 className="text-xl font-bold text-gray-800 mb-4 text-center">
//                   {currentScene.question}
//                 </h3>
//                 <div className="space-y-3">
//                   {currentScene.choices.map((choice, index) => (
//                     <button
//                       key={index}
//                       onClick={() => makeChoice(choice)}
//                       disabled={loading}
//                       className="w-full bg-blue-500 hover:bg-blue-600 text-white font-semibold py-4 px-6 rounded-lg text-lg transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed text-center"
//                     >
//                       {loading ? t.thinking : choice}
//                     </button>
//                   ))}
//                 </div>
//               </div>

//             </div>

//             {loading && (
//               <div className="bg-white rounded-2xl shadow-xl p-8 text-center">
//                 <div className="text-purple-500 flex justify-center mb-4">
//                   <LoaderIcon className="h-12 w-12" />
//                 </div>
//                 <p className="text-lg text-gray-700">{t.loadingNextScene}</p>
//               </div>
//             )}

//           </div>
//         )}

//       </div>
//     </div>
//   );
// }



// import React, { useState, useRef, useEffect } from 'react';

// // (Imports and translations remain the same)
// const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

// const translations = {
//   en: {
//     title: "AI Story Builder",
//     subtitle: "Synced video & narration! 🎬🎙️",
//     errorPrefix: "Oops!",
//     startTitle: "Let's start a new adventure!",
//     placeholder: "e.g., A brave knight and a funny dragon",
//     suggestionHeader: "Or try one of these ideas:",
//     suggestions: [
//       "sun with the moon",
//       "a brave knight and friendly dragon",
//       "a little girl and bear"
//     ],
//     startStory: "Start My Story! 🚀",
//     loadingStart: "Creating your story...",
//     loadingScene: "Creating your magical scene...",
//     loadingSceneSub: "Generating synced video and narration ✨",
//     videoLoading: "Video is loading...",
//     titlePause: "Pause",
//     titlePlay: "Play",
//     titleMute: "Mute video",
//     titleUnmute: "Unmute video",
//     replay: "Replay",
//     titleFullscreenEnter: "Enter Fullscreen",
//     titleFullscreenExit: "Exit Fullscreen",
//     titleSubtitlesOn: "Hide Subtitles",
//     titleSubtitlesOff: "Show Subtitles",
//     narratorLabel: "Narrator:",
//     narrating: "Narrating...",
//     thinking: "Thinking...",
//     loadingNextScene: "Creating the next scene with narration...",
//     reset: "Start a New Story"
//   },
//   mr: {
//     title: "AI कथा निर्माता",
//     subtitle: "सिंक केलेला व्हिडिओ आणि निवेदन! 🎬🎙️",
//     errorPrefix: "अरे!",
//     startTitle: "चला एक नवीन साहस सुरू करूया!",
//     placeholder: "उदा. एक शूर योद्धा आणि एक मजेदार ड्रॅगन",
//     suggestionHeader: "किंवा यापैकी एक कल्पना वापरून पहा:",
//     suggestions: [
//       "सूर्य आणि चंद्र",
//       "एक शूर योद्धा आणि एक मित्र ड्रॅगन",
//       "एक लहान मुलगी आणि अस्वल"
//     ],
//     startStory: "माझी कथा सुरू करा! 🚀",
//     loadingStart: "तुमची कथा तयार करत आहे...",
//     loadingScene: "तुमचे जादुई दृश्य तयार करत आहे...",
//     loadingSceneSub: "सिंक केलेला व्हिडिओ आणि निवेदन तयार होत आहे ✨",
//     videoLoading: "व्हिडिओ लोड होत आहे...",
//     titlePause: "विराम",
//     titlePlay: "प्ले",
//     titleMute: "व्हिडिओ म्यूट करा",
//     titleUnmute: "व्हिडिओ अनम्यूट करा",
//     replay: "पुन्हा प्ले करा",
//     titleFullscreenEnter: "पूर्णस्क्रीन",
//     titleFullscreenExit: "पूर्णस्क्रीनमधून बाहेर पडा",
//     titleSubtitlesOn: "उपशीर्षके लपवा",
//     titleSubtitlesOff: "उपशीर्षके दर्शवा",
//     narratorLabel: "निवेदक:",
//     narrating: "निवेदन करत आहे...",
//     thinking: "विचार करत आहे...",
//     loadingNextScene: "पुढील दृश्य निवेदनासह तयार करत आहे...",
//     reset: "नवीन कथा सुरू करा"
//   }
// };

// const enToMrSuggestionsMap = {
//   "sun with the moon": "सूर्य आणि चंद्र",
//   "a brave knight and friendly dragon": "एक शूर योद्धा आणि एक मित्र ड्रॅगन",
//   "a tortoise and rabbit": "कासव आणि ससा",
//   "a little girl and bear": "एक लहान मुलगी आणि अस्वल",
//   "the monkey and the crocodile": "माकड आणि मगर",
//   "stork and crab": "सारस आणि खेकडा"
// };

// // (All Icon components remain the same...)
// const SparklesIcon = () => (
//   <svg className="w-10 h-10" fill="currentColor" viewBox="0 0 24 24">
//     <path d="M12 0l1.545 5.633L19 7.5l-5.455 1.867L12 15l-1.545-5.633L5 7.5l5.455-1.867L12 0zM4 12l1.029 3.756L9 17l-3.971 1.244L4 22l-1.029-3.756L0 17l3.971-1.244L4 12zm16 0l1.029 3.756L25 17l-3.971 1.244L20 22l-1.029-3.756L16 17l3.971-1.244L20 12z"/>
//   </svg>
// );
// const VideoIcon = () => (
//   <svg className="w-16 h-16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
//     <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
//   </svg>
// );
// const LoaderIcon = ({ className = "h-12 w-12" }) => (
//   <svg className={`animate-spin ${className}`} fill="none" viewBox="0 0 24 24">
//     <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
//     <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
//   </svg>
// );
// const ResetIcon = () => (
//   <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
//     <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
//   </svg>
// );
// const VolumeIcon = () => (
//   <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
//     <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
//   </svg>
// );
// const VolumeMuteIcon = () => (
//   <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
//     <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z M17 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2" />
//   </svg>
// );
// const PlayIcon = () => (
//   <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
//     <path d="M8 5v14l11-7z" />
//   </svg>
// );
// const PauseIcon = () => (
//   <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
//     <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z" />
//   </svg>
// );
// const FullscreenEnterIcon = () => (
//   <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
//     <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 8V4h4m12 4V4h-4M4 16v4h4m12-4v4h-4" />
//   </svg>
// );
// const FullscreenExitIcon = () => (
//   <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
//     <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 4H4v4m12-4h4v4M8 20H4v-4m12 4h4v-4" />
//   </svg>
// );
// const CCIcon = () => (
//     <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
//         <path d="M20 4H4C2.9 4 2 4.9 2 6v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zM9.5 15c0 .83-.67 1.5-1.5 1.5H6.5c-.83 0-1.5-.67-1.5-1.5v-3c0-.83.67-1.5 1.5-1.5h1.5c.83 0 1.5.67 1.5 1.5v3zm7 0c0 .83-.67 1.5-1.5 1.5h-1.5c-.83 0-1.5-.67-1.5-1.5v-3c0-.83.67-1.5 1.5-1.5h1.5c.83 0 1.5.67 1.5 1.5v3z"/>
//     </svg>
// );
// const CCOffIcon = () => (
//     <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
//         <path d="M2.81 2.81L1.39 4.22L3 5.83V18c0 1.1.9 2 2 2h12.17l2.61 2.61l1.41-1.41L2.81 2.81zM5 18V7.83l10.17 10.17H5zm15-1.17L10.83 8H16.5c.83 0 1.5.67 1.5 1.5v3c0 .83-.67 1.5-1.5 1.5h-1.5v-1.5h1.5v-3H15v1.17l-3-3V9c0-.83.67-1.5 1.5-1.5h1.5c.83 0 1.5.67 1.5 1.5v.17l4.78 4.78C20 13.65 20 13.34 20 13v-3c0-1.1-.9-2-2-2H9.83l-4-4H20c1.1 0 2 .9 2 2v12c0 .35-.09.68-.24.97l-1.6-1.6C19.9 17.54 20 17.77 20 18v-4.17zM9.5 15c0 .83-.67 1.5-1.5 1.5H6.5c-.83 0-1.5-.67-1.5-1.5v-3c0-.83.67-1.5 1.5-1.5h1.5c.83 0 1.5.67 1.5 1.5v3z"/>
//     </svg>
// );


// const formatTime = (timeInSeconds) => {
//   if (isNaN(timeInSeconds) || timeInSeconds === 0) return "0:00";
//   const minutes = Math.floor(timeInSeconds / 60);
//   const seconds = Math.floor(timeInSeconds % 60);
//   return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
// };

// export default function CartoonStoryBuilder() {
//   const [storyState, setStoryState] = useState('initial');
//   const [initialIdea, setInitialIdea] = useState('');
//   const [currentScene, setCurrentScene] = useState(null);
//   const [videoUrl, setVideoUrl] = useState(null);
//   const [audioUrl, setAudioUrl] = useState(null);
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState(null);
//   const [sessionId, setSessionId] = useState(null);
//   const [isNarrating, setIsNarrating] = useState(false);
//   const [videoVolume, setVideoVolume] = useState(0.1);
//   const [isVideoReady, setIsVideoReady] = useState(false);
//   const [isAudioReady, setIsAudioReady] = useState(false);
//   const [isPlaying, setIsPlaying] = useState(false);
//   const [isFullscreen, setIsFullscreen] = useState(false);
//   const [language, setLanguage] = useState('en');
//   const [duration, setDuration] = useState(0);
//   const [currentTime, setCurrentTime] = useState(0);
//   const [buffered, setBuffered] = useState(0);
//   const [showSubtitles, setShowSubtitles] = useState(true);
//   const t = translations[language]; 
//   const [subtitleWords, setSubtitleWords] = useState([]);
//   const [visibleSubtitle, setVisibleSubtitle] = useState('');
  
//   // ======================================================================================
//   // *** BEGIN FRONTEND FIX 1/4 ***
//   // ======================================================================================
//   const [hasEnded, setHasEnded] = useState(false); 
//   // ======================================================================================
//   // *** END FRONTEND FIX 1/4 ***
//   // ======================================================================================
  
//   const [debouncedIdea, setDebouncedIdea] = useState(initialIdea);
//   const [isTranslating, setIsTranslating] = useState(false);
//   const isMounted = useRef(false); 
//   const audioRef = useRef(null);
//   const videoRef = useRef(null);
//   const playerContainerRef = useRef(null);

//   // (All useEffects and handler functions remain the same...)
//   useEffect(() => {
//     const onFullscreenChange = () => {
//       setIsFullscreen(!!document.fullscreenElement);
//     };
//     document.addEventListener('fullscreenchange', onFullscreenChange);
//     return () => document.removeEventListener('fullscreenchange', onFullscreenChange);
//   }, []);

//   useEffect(() => {
//     if (videoUrl) {
//       setIsVideoReady(false);
//       setIsAudioReady(false); 
//       setCurrentTime(0);
//       setDuration(0);
//       setBuffered(0);
//       // ======================================================================================
//       // *** BEGIN FRONTEND FIX 2/4 ***
//       // ======================================================================================
//       setHasEnded(false); 
//       // ======================================================================================
//       // *** END FRONTEND FIX 2/4 ***
//       // ======================================================================================
//       if (videoRef.current) {
//         videoRef.current.pause();
//         videoRef.current.currentTime = 0;
//       }
//       if (audioRef.current) {
//         audioRef.current.pause();
//         audioRef.current.currentTime = 0;
//       }
//       if (!audioUrl) {
//         setIsAudioReady(true);
//       }
//     }
//   }, [audioUrl, videoUrl]);

//   useEffect(() => {
//     const canPlay = isVideoReady && (isAudioReady || !audioUrl) && videoRef.current;
//     if (canPlay) {
//       const playMedia = async () => {
//         try {
//           videoRef.current.volume = videoVolume;
//           if (audioRef.current) {
//             await Promise.all([
//               videoRef.current.play(),
//               audioRef.current.play()
//             ]);
//           } else {
//             await videoRef.current.play();
//           }
//         } catch (error) {
//           console.error('Error starting playback:', error);
//         }
//       };
//       playMedia();
//     }
//   }, [isVideoReady, isAudioReady, videoVolume, audioUrl]);

//   useEffect(() => {
//     if (currentScene?.story_text) {
//       setSubtitleWords(currentScene.story_text.split(' '));
//       setVisibleSubtitle(''); // Reset on new scene
//     } else {
//       setSubtitleWords([]);
//       setVisibleSubtitle('');
//     }
//   }, [currentScene]);

//   useEffect(() => {
//     const handler = setTimeout(() => {
//       setDebouncedIdea(initialIdea);
//     }, 1200);

//     return () => {
//       clearTimeout(handler);
//     };
//   }, [initialIdea]);

//   useEffect(() => {
//     if (!isMounted.current) {
//       isMounted.current = true;
//       return;
//     }
//     const translateIdea = async () => {
//       if (language === 'mr' && debouncedIdea.trim()) {
//         const hardcodedTranslation = enToMrSuggestionsMap[debouncedIdea.trim().toLowerCase()];
//         if (hardcodedTranslation) {
//           if (hardcodedTranslation !== initialIdea) {
//             setInitialIdea(hardcodedTranslation);
//           }
//           return; 
//         }
//         setIsTranslating(true);
//         try {
//           const response = await fetch(`${API_BASE_URL}/api/translate`, {
//             method: 'POST',
//             headers: { 'Content-Type': 'application/json' },
//             body: JSON.stringify({ text: debouncedIdea, target_lang: 'mr' })
//           });
//           if (!response.ok) {
//             const errData = await response.json().catch(() => ({}));
//             throw new Error(errData.detail || 'Translation service failed');
//           }
//           const data = await response.json();
//           if (data.translated_text && data.translated_text !== initialIdea) {
//             setInitialIdea(data.translated_text);
//           }
//         } catch (err) {
//           console.error("Translation error:", err.message);
//         } finally {
//           setIsTranslating(false);
//         }
//       }
//     };
//     translateIdea();
//   }, [debouncedIdea, language]);

//   const handlePlaybackChange = (playing) => {
//     setIsNarrating(playing);
//     setIsPlaying(playing);
//   };
//   const togglePlayPause = () => {
//     if (!videoRef.current) return;
//     if (isPlaying) {
//       videoRef.current.pause();
//       if (audioRef.current) {
//         audioRef.current.pause();
//       }
//     } else {
//       videoRef.current.play();
//       if (audioRef.current) {
//         audioRef.current.play();
//       }
//     }
//   };
//   const toggleVideoVolume = () => {
//     const newVolume = videoVolume > 0 ? 0 : 0.1;
//     setVideoVolume(newVolume);
//     if (videoRef.current) {
//       videoRef.current.volume = newVolume;
//     }
//   };
//   const replayScene = () => {
//     if (videoRef.current) {
//       // ======================================================================================
//       // *** BEGIN FRONTEND FIX 3/4 ***
//       // ======================================================================================
//       setHasEnded(false); 
//       // ======================================================================================
//       // *** END FRONTEND FIX 3/4 ***
//       // ======================================================================================
//       setIsVideoReady(false);
//       setIsAudioReady(false);
//       setCurrentTime(0);
//       setVisibleSubtitle(''); // Reset visible words
//       videoRef.current.currentTime = 0;
//       if (audioRef.current) {
//         audioRef.current.currentTime = 0;
//       }
//       if (!audioUrl) {
//         setIsAudioReady(true);
//       }
//     }
//   };
//   const toggleFullscreen = () => {
//     if (!document.fullscreenElement) {
//       playerContainerRef.current?.requestFullscreen().catch(err => {
//         alert(`Error attempting to enable full-screen mode: ${err.message} (${err.name})`);
//       });
//     } else {
//       document.exitFullscreen();
//     }
//   };
//   const handleSeek = (e) => {
//     if (!videoRef.current || isNaN(duration) || duration === 0) return;
//     // ======================================================================================
//     // *** BEGIN FRONTEND FIX 3/4 (Duplicate) ***
//     // ======================================================================================
//     setHasEnded(false); 
//     // ======================================================================================
//     // *** END FRONTEND FIX 3/4 (Duplicate) ***
//     // ======================================================================================
//     const progressBar = e.currentTarget;
//     const clickPosition = e.nativeEvent.offsetX;
//     const barWidth = progressBar.clientWidth;
//     const seekTime = (clickPosition / barWidth) * duration;
//     videoRef.current.currentTime = seekTime;
//     if(audioRef.current) {
//       audioRef.current.currentTime = seekTime;
//     }
//     setCurrentTime(seekTime);
//   };
//   const executeStartStory = async (prompt) => {
//     if (!prompt.trim()) return;
//     setLoading(true);
//     setError(null);
//     setStoryState('loading');
//     try {
//       const response = await fetch(`${API_BASE_URL}/api/start-story`, {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({ 
//           initial_idea: prompt,
//           language: language
//         })
//       });
//       if (!response.ok) {
//         const errorData = await response.json().catch(() => ({}));
//         throw new Error(errorData.detail || `Failed to start story`);
//       }
//       const data = await response.json();
//       setSessionId(data.session_id);
//       setCurrentScene(data.story_part);
//       setVideoUrl(data.video_url);
//       setAudioUrl(data.audio_url);
//       setStoryState('scene');
//     } catch (err) {
//       setError(err.message);
//       setStoryState('initial');
//     } finally {
//       setLoading(false);
//     }
//   };
//   const startStory = async () => {
//     executeStartStory(initialIdea);
//   };
//   const handleSuggestionClick = (suggestion) => {
//     setInitialIdea(suggestion); 
//     executeStartStory(suggestion); 
//   };
//   const makeChoice = async (choice) => {
//     setLoading(true);
//     setError(null);
//     try {
//       const response = await fetch(`${API_BASE_URL}/api/continue-story`, {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({ 
//           session_id: sessionId, 
//           choice: choice,
//           language: language
//         })
//       });
//       if (!response.ok) {
//         const errorData = await response.json().catch(() => ({}));
//         throw new Error(errorData.detail || `Failed to continue story`);
//       }
//       const data = await response.json();
//       setCurrentScene(data.story_part);
//       setVideoUrl(data.video_url);
//       setAudioUrl(data.audio_url);
//     } catch (err) {
//       setError(err.message);
//     } finally {
//       setLoading(false);
//     }
//   };
//   const handleFullReset = async () => {
//      try {
//       await fetch(`${API_BASE_URL}/api/reset`, { 
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({ session_id: null }) // Resets *all* sessions
//       });
//       alert('All story sessions have been reset!');
//     } catch (err) {
//       console.error('Full reset failed:', err);
//       alert('Could not reset sessions.');
//     }
//   };

//   return (
//     <div className="min-h-screen bg-gradient-to-br from-purple-100 via-pink-100 to-blue-100 p-4 font-sans">
//       <div className="max-w-6xl mx-auto">
        
//         <div className="text-center mb-8 pt-8">
//           <h1 className="text-5xl font-bold text-purple-600 mb-2 flex items-center justify-center gap-3">
//             <SparklesIcon />
//             {t.title} 
//             <SparklesIcon />
//           </h1>
//           <p className="text-gray-600 text-lg">{t.subtitle}</p>
//         </div>

//         {audioUrl && (
//           <audio
//             ref={audioRef}
//             src={`${API_BASE_URL}${audioUrl}`}
//             onCanPlayThrough={() => setIsAudioReady(true)}
//             onPlay={() => handlePlaybackChange(true)}
//             // ======================================================================================
//             // *** BEGIN FRONTEND FIX 4/4 ***
//             // ======================================================================================
//             onEnded={() => {
//               handlePlaybackChange(false);
//               setHasEnded(true); 
//             }}
//             // ======================================================================================
//             // *** END FRONTEND FIX 4/4 ***
//             // ======================================================================================
//             onPause={() => handlePlaybackChange(false)}
//           />
//         )}


//         {error && (
//           <div className="bg-red-100 border-2 border-red-400 rounded-lg p-4 mb-6">
//             <p className="text-red-700 font-semibold">{t.errorPrefix}! {error}</p>
//           </div>
//         )}

//         {storyState === 'initial' && (
//           <div className="bg-white rounded-2xl shadow-xl p-8 mb-6">
            
//             <div className="flex justify-between items-center mb-4">
//                 <h2 className="text-2xl font-bold text-gray-800">
//                   {t.startTitle}
//                 </h2>
//                 <select 
//                   value={language} 
//                   onChange={(e) => setLanguage(e.target.value)}
//                   className="bg-white border-2 border-purple-300 rounded-lg px-3 py-2 text-purple-700 font-medium focus:outline-none focus:border-purple-500"
//                 >
//                   <option value="en">English</option>
//                   <option value="mr">मराठी (Marathi)</option>
//                 </select>
//             </div>

//             <div className="relative">
//               <input
//                 type="text"
//                 value={initialIdea}
//                 onChange={(e) => setInitialIdea(e.target.value)}
//                 placeholder={t.placeholder}
//                 className="w-full px-4 py-3 border-2 border-purple-300 rounded-lg mb-4 text-lg focus:outline-none focus:border-purple-500"
//                 onKeyPress={(e) => e.key === 'Enter' && startStory()}
//               />
//               {isTranslating && (
//                 <div className="absolute right-4 top-1/2 -translate-y-1/2" style={{top: '1.1rem'}}>
//                   <LoaderIcon className="h-5 w-5 text-purple-400" />
//                 </div>
//               )}
//             </div>


//             <div className="my-4">
//               <p className="text-base text-gray-500 mb-2 text-center">{t.suggestionHeader}</p>
//               <div className="flex flex-wrap justify-center gap-2">
//                 {t.suggestions.map((suggestion) => (
//                   <button
//                     key={suggestion}
//                     onClick={() => handleSuggestionClick(suggestion)}
//                     disabled={loading}
//                     className="px-6 py-3 bg-purple-50 hover:bg-purple-100 text-purple-600 font-medium rounded-full text-base transition-all disabled:opacity-50 disabled:cursor-not-allowed"
//                   >
//                     {suggestion}
//                   </button>
//                 ))}
//               </div>
//             </div>
            
//             <button
//               onClick={startStory}
//               disabled={!initialIdea.trim() || loading || isTranslating}
//               className="w-full bg-gradient-to-r from-purple-500 to-pink-500 text-white font-bold py-3 rounded-lg text-lg hover:from-purple-600 hover:to-pink-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:scale-105 mt-4"
//             >
//               {loading ? t.loadingStart : (isTranslating ? 'Translating...' : t.startStory)}
//             </button>
            
//           </div>
//         )}

        
//         {storyState === 'loading' && (
//           <div className="bg-white rounded-2xl shadow-xl p-12 text-center">
//             <div className="text-purple-500 flex justify-center mb-4">
//               <LoaderIcon className="h-12 w-12" />
//             </div>
//             <h3 className="text-2xl font-bold text-gray-800 mb-2">
//               {t.loadingScene}
//             </h3>
//             <p className="text-gray-600">{t.loadingSceneSub}</p>
//           </div>
//         )}

//         {storyState === 'scene' && currentScene && (
//           <div className="space-y-6">

//             <div className="space-y-6">
            
//               {/* --- THIS IS THE UPDATED LINE --- */}
//               <div ref={playerContainerRef} className="bg-white rounded-2xl shadow-xl p-6 max-w-3xl mx-auto">
//                 {videoUrl ? (
//                   <div className="relative">
//                     <video
//                       ref={videoRef}
//                       key={videoUrl}
//                       loop
//                       playsInline
//                       className="w-full rounded-lg shadow-lg bg-black cursor-pointer"
//                       src={`${API_BASE_URL}${videoUrl}`}
//                       onCanPlayThrough={() => setIsVideoReady(true)}
//                       onClick={togglePlayPause}
//                       onLoadedMetadata={() => setDuration(videoRef.current.duration)}
//                       onTimeUpdate={() => {
//                         if (!videoRef.current) return;
//                         const time = videoRef.current.currentTime;
//                         setCurrentTime(time);
//                         if (videoRef.current.buffered.length > 0) {
//                           setBuffered(videoRef.current.buffered.end(videoRef.current.buffered.length - 1));
//                         }
//                         if (duration > 0 && subtitleWords.length > 0) {
//                           const timePerWord = duration / subtitleWords.length;
//                           const wordCountToShow = Math.floor(time / timePerWord) + 1;
//                           const visibleWords = subtitleWords.slice(0, wordCountToShow).join(' ');
//                           setVisibleSubtitle(visibleWords);
//                         }
//                       }}
//                     />
                    
//                     {showSubtitles && currentScene && (
//                       <div 
//                         className="absolute bottom-16 md:bottom-20 left-1/2 -translate-x-1/2 w-full px-4 pointer-events-none"
//                       >
//                         <p 
//                           className="text-center text-lg md:text-2xl font-semibold text-white"
//                           style={{ textShadow: '2px 2px 4px rgba(0, 0, 0, 0.8)' }} 
//                         >
//                           {visibleSubtitle}
//                         </p>
//                       </div>
//                     )}
                    
//                     <div className="absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-black/60 to-transparent">
//                       <div 
//                         className="relative w-full h-1.5 bg-white/20 rounded-full cursor-pointer"
//                         onClick={handleSeek}
//                       >
//                         <div 
//                           className="absolute left-0 top-0 h-full bg-white/40 rounded-full" 
//                           style={{ width: `${(buffered / duration) * 100}%` }} 
//                         />
//                         <div 
//                           className="absolute left-0 top-0 h-full bg-pink-500 rounded-full" 
//                           style={{ width: `${(currentTime / duration)* 100}%` }} 
//                         />
//                       </div>
                      
//                       <div className="flex justify-between items-center mt-2 text-white">
//                         {/* ====================================================================================== */}
//                         {/* *** BEGIN FRONTEND FIX (FINAL BUTTON REPLACEMENT) *** */}
//                         {/* ====================================================================================== */}
//                         <div className="flex gap-2 items-center">
//                           <button
//                             onClick={hasEnded ? replayScene : togglePlayPause}
//                             className="bg-transparent hover:bg-black/70 text-white p-2 rounded-full transition-all"
//                             title={isPlaying ? t.titlePause : (hasEnded ? t.replay : t.titlePlay)}
//                           >
//                             {isPlaying ? <PauseIcon /> : (hasEnded ? <ResetIcon /> : <PlayIcon />)}
//                           </button>
//                           <button
//                             onClick={toggleVideoVolume}
//                             className="bg-transparent hover:bg-black/70 text-white p-2 rounded-full transition-all"
//                             title={videoVolume > 0 ? t.titleMute : t.titleUnmute}
//                           >
//                             {videoVolume > 0 ? <VolumeIcon /> : <VolumeMuteIcon />}
//                           </button>
//                         </div>
//                         {/* ====================================================================================== */}
//                         {/* *** END FRONTEND FIX (FINAL BUTTON REPLACEMENT) *** */}
//                         {/* ====================================================================================== */}
                        
//                         <div className="text-sm font-medium">
//                           {formatTime(currentTime)} / {formatTime(duration)}
//                         </div>
                        
//                         <div className="flex gap-2 items-center">
//                           <button
//                             onClick={() => setShowSubtitles(!showSubtitles)}
//                             className={`bg-transparent hover:bg-black/70 p-2 rounded-full transition-all ${
//                               showSubtitles ? 'text-pink-400' : 'text-white'
//                             }`}
//                             title={showSubtitles ? t.titleSubtitlesOn : t.titleSubtitlesOff}
//                           >
//                             {showSubtitles ? <CCIcon /> : <CCOffIcon />}
//                           </button>
//                           <button
//                             onClick={toggleFullscreen}
//                             className="bg-transparent hover:bg-black/70 text-white p-2 rounded-full transition-all"
//                             title={isFullscreen ? t.titleFullscreenExit : t.titleFullscreenEnter}
//                           >
//                             {isFullscreen ? <FullscreenExitIcon /> : <FullscreenEnterIcon />}
//                           </button>
//                         </div>
//                       </div>
//                     </div>
//                   </div>
//                 ) : (
//                   <div className="bg-gray-100 rounded-lg p-12 text-center">
//                     <div className="text-gray-400 flex justify-center mb-4">
//                       <VideoIcon />
//                     </div>
//                     <p className="text-gray-600">{t.videoLoading}</p>
//                   </div>
//                 )}
//               </div>

//               {/* --- THIS IS THE UPDATED LINE --- */}
//               <div className="bg-white rounded-2xl shadow-xl p-6 max-w-3xl mx-auto">
//                 <h3 className="text-xl font-bold text-gray-800 mb-4 text-center">
//                   {currentScene.question}
//                 </h3>
//                 <div className="space-y-3">
//                   {currentScene.choices.map((choice, index) => (
//                     <button
//                       key={index}
//                       onClick={() => makeChoice(choice)}
//                       disabled={loading}
//                       className="w-full bg-blue-500 hover:bg-blue-600 text-white font-semibold py-4 px-6 rounded-lg text-lg transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed text-center"
//                     >
//                       {loading ? t.thinking : choice}
//                     </button>
//                   ))}
//                 </div>
//               </div>

//             </div>

//             {loading && (
//               <div className="bg-white rounded-2xl shadow-xl p-8 text-center">
//                 <div className="text-purple-500 flex justify-center mb-4">
//                   <LoaderIcon className="h-12 w-12" />
//                 </div>
//                 <p className="text-lg text-gray-700">{t.loadingNextScene}</p>
//               </div>
//             )}

//           </div>
//         )}

//       </div>
//     </div>
//   );
// }


import React, { useState, useRef, useEffect } from 'react';

// (Imports and translations remain the same)
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

const translations = {
  en: {
    title: "AI Story Builder",
    subtitle: "Synced video & narration! 🎬🎙️",
    errorPrefix: "Oops!",
    startTitle: "Let's start a new adventure!",
    placeholder: "e.g., A brave knight and a funny dragon",
    suggestionHeader: "Or try one of these ideas:",
    suggestions: [
      "sun with the moon",
      "a brave knight and friendly dragon",
      "a little girl and bear"
    ],
    startStory: "Start My Story! 🚀",
    loadingStart: "Creating your story...",
    loadingScene: "Creating your magical scene...",
    loadingSceneSub: "Generating synced video and narration ✨",
    videoLoading: "Video is loading...",
    titlePause: "Pause",
    titlePlay: "Play",
    titleMute: "Mute video",
    titleUnmute: "Unmute video",
    replay: "Replay",
    titleFullscreenEnter: "Enter Fullscreen",
    titleFullscreenExit: "Exit Fullscreen",
    titleSubtitlesOn: "Hide Subtitles",
    titleSubtitlesOff: "Show Subtitles",
    narratorLabel: "Narrator:",
    narrating: "Narrating...",
    thinking: "Thinking...",
    loadingNextScene: "Creating the next scene with narration...",
    reset: "Start a New Story"
  },
  mr: {
    title: "AI कथा निर्माता",
    subtitle: "सिंक केलेला व्हिडिओ आणि निवेदन! 🎬🎙️",
    errorPrefix: "अरे!",
    startTitle: "चला एक नवीन साहस सुरू करूया!",
    placeholder: "उदा. एक शूर योद्धा आणि एक मजेदार ड्रॅगन",
    suggestionHeader: "किंवा यापैकी एक कल्पना वापरून पहा:",
    suggestions: [
      "सूर्य आणि चंद्र",
      "एक शूर योद्धा आणि एक मित्र ड्रॅगन",
      "एक लहान मुलगी आणि अस्वल"
    ],
    startStory: "माझी कथा सुरू करा! 🚀",
    loadingStart: "तुमची कथा तयार करत आहे...",
    loadingScene: "तुमचे जादुई दृश्य तयार करत आहे...",
    loadingSceneSub: "सिंक केलेला व्हिडिओ आणि निवेदन तयार होत आहे ✨",
    videoLoading: "व्हिडिओ लोड होत आहे...",
    titlePause: "विराम",
    titlePlay: "प्ले",
    titleMute: "व्हिडिओ म्यूट करा",
    titleUnmute: "व्हिडिओ अनम्यूट करा",
    replay: "पुन्हा प्ले करा",
    titleFullscreenEnter: "पूर्णस्क्रीन",
    titleFullscreenExit: "पूर्णस्क्रीनमधून बाहेर पडा",
    titleSubtitlesOn: "उपशीर्षके लपवा",
    titleSubtitlesOff: "उपशीर्षके दर्शवा",
    narratorLabel: "निवेदक:",
    narrating: "निवेदन करत आहे...",
    thinking: "विचार करत आहे...",
    loadingNextScene: "पुढील दृश्य निवेदनासह तयार करत आहे...",
    reset: "नवीन कथा सुरू करा"
  }
};

const enToMrSuggestionsMap = {
  "sun with the moon": "सूर्य आणि चंद्र",
  "a brave knight and friendly dragon": "एक शूर योद्धा आणि एक मित्र ड्रॅगन",
  "a tortoise and rabbit": "कासव आणि ससा",
  "a little girl and bear": "एक लहान मुलगी आणि अस्वल",
  "the monkey and the crocodile": "माकड आणि मगर",
  "stork and crab": "सारस आणि खेकडा"
};

// (All Icon components remain the same...)
const SparklesIcon = () => (
  <svg className="w-10 h-10" fill="currentColor" viewBox="0 0 24 24">
    <path d="M12 0l1.545 5.633L19 7.5l-5.455 1.867L12 15l-1.545-5.633L5 7.5l5.455-1.867L12 0zM4 12l1.029 3.756L9 17l-3.971 1.244L4 22l-1.029-3.756L0 17l3.971-1.244L4 12zm16 0l1.029 3.756L25 17l-3.971 1.244L20 22l-1.029-3.756L16 17l3.971-1.244L20 12z"/>
  </svg>
);
const VideoIcon = () => (
  <svg className="w-16 h-16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
  </svg>
);
const LoaderIcon = ({ className = "h-12 w-12" }) => (
  <svg className={`animate-spin ${className}`} fill="none" viewBox="0 0 24 24">
    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
  </svg>
);
const ResetIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
  </svg>
);
const VolumeIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
  </svg>
);
const VolumeMuteIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z M17 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2" />
  </svg>
);
const PlayIcon = () => (
  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
    <path d="M8 5v14l11-7z" />
  </svg>
);
const PauseIcon = () => (
  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
    <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z" />
  </svg>
);
const FullscreenEnterIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 8V4h4m12 4V4h-4M4 16v4h4m12-4v4h-4" />
  </svg>
);
const FullscreenExitIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 4H4v4m12-4h4v4M8 20H4v-4m12 4h4v-4" />
  </svg>
);
const CCIcon = () => (
    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
        <path d="M20 4H4C2.9 4 2 4.9 2 6v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zM9.5 15c0 .83-.67 1.5-1.5 1.5H6.5c-.83 0-1.5-.67-1.5-1.5v-3c0-.83.67-1.5 1.5-1.5h1.5c.83 0 1.5.67 1.5 1.5v3zm7 0c0 .83-.67 1.5-1.5 1.5h-1.5c-.83 0-1.5-.67-1.5-1.5v-3c0-.83.67-1.5 1.5-1.5h1.5c.83 0 1.5.67 1.5 1.5v3z"/>
    </svg>
);
const CCOffIcon = () => (
    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
        <path d="M2.81 2.81L1.39 4.22L3 5.83V18c0 1.1.9 2 2 2h12.17l2.61 2.61l1.41-1.41L2.81 2.81zM5 18V7.83l10.17 10.17H5zm15-1.17L10.83 8H16.5c.83 0 1.5.67 1.5 1.5v3c0 .83-.67 1.5-1.5 1.5h-1.5v-1.5h1.5v-3H15v1.17l-3-3V9c0-.83.67-1.5 1.5-1.5h1.5c.83 0 1.5.67 1.5 1.5v.17l4.78 4.78C20 13.65 20 13.34 20 13v-3c0-1.1-.9-2-2-2H9.83l-4-4H20c1.1 0 2 .9 2 2v12c0 .35-.09.68-.24.97l-1.6-1.6C19.9 17.54 20 17.77 20 18v-4.17zM9.5 15c0 .83-.67 1.5-1.5 1.5H6.5c-.83 0-1.5-.67-1.5-1.5v-3c0-.83.67-1.5 1.5-1.5h1.5c.83 0 1.5.67 1.5 1.5v3z"/>
    </svg>
);

// === NEW: MicrophoneIcon ===
const MicrophoneIcon = () => (
  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
    <path d="M12 14c1.66 0 2.99-1.34 2.99-3L15 5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm-1.2-9.1c0-.66.54-1.2 1.2-1.2.66 0 1.2.54 1.2 1.2l-.01 6.2c0 .66-.53 1.2-1.19 1.2-.66 0-1.2-.54-1.2-1.2V4.9zm6.5 6.1c0 3-2.54 5.1-5.3 5.1S6.7 14 6.7 11H5c0 3.41 2.72 6.23 6 6.72V21h2v-3.28c3.28-.49 6-3.31 6-6.72h-1.7z" />
  </svg>
);


const formatTime = (timeInSeconds) => {
  if (isNaN(timeInSeconds) || timeInSeconds === 0) return "0:00";
  const minutes = Math.floor(timeInSeconds / 60);
  const seconds = Math.floor(timeInSeconds % 60);
  return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
};

export default function CartoonStoryBuilder() {
  const [storyState, setStoryState] = useState('initial');
  const [initialIdea, setInitialIdea] = useState('');
  const [currentScene, setCurrentScene] = useState(null);
  const [videoUrl, setVideoUrl] = useState(null);
  const [audioUrl, setAudioUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [isNarrating, setIsNarrating] = useState(false);
  const [videoVolume, setVideoVolume] = useState(0.1);
  const [isVideoReady, setIsVideoReady] = useState(false);
  const [isAudioReady, setIsAudioReady] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [language, setLanguage] = useState('en');
  const [duration, setDuration] = useState(0);
  const [currentTime, setCurrentTime] = useState(0);
  const [buffered, setBuffered] = useState(0);
  const [showSubtitles, setShowSubtitles] = useState(true);
  const t = translations[language]; 
  const [subtitleWords, setSubtitleWords] = useState([]);
  const [visibleSubtitle, setVisibleSubtitle] = useState('');
  
  // ======================================================================================
  // *** BEGIN FRONTEND FIX 1/4 ***
  // ======================================================================================
  const [hasEnded, setHasEnded] = useState(false); 
  // ======================================================================================
  // *** END FRONTEND FIX 1/4 ***
  // ======================================================================================
  
  const [debouncedIdea, setDebouncedIdea] = useState(initialIdea);
  const [isTranslating, setIsTranslating] = useState(false);

  // === NEW: state and refs for recording ===
  const [isRecording, setIsRecording] = useState(false);
  const [isTranscribing, setIsTranscribing] = useState(false);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  // === END OF NEW ===
  
  const isMounted = useRef(false); 
  const audioRef = useRef(null);
  const videoRef = useRef(null);
  const playerContainerRef = useRef(null);

  // (All useEffects and handler functions remain the same...)
  useEffect(() => {
    const onFullscreenChange = () => {
      setIsFullscreen(!!document.fullscreenElement);
    };
    document.addEventListener('fullscreenchange', onFullscreenChange);
    return () => document.removeEventListener('fullscreenchange', onFullscreenChange);
  }, []);

  useEffect(() => {
    if (videoUrl) {
      setIsVideoReady(false);
      setIsAudioReady(false); 
      setCurrentTime(0);
      setDuration(0);
      setBuffered(0);
      // ======================================================================================
      // *** BEGIN FRONTEND FIX 2/4 ***
      // ======================================================================================
      setHasEnded(false); 
      // ======================================================================================
      // *** END FRONTEND FIX 2/4 ***
      // ======================================================================================
      if (videoRef.current) {
        videoRef.current.pause();
        videoRef.current.currentTime = 0;
      }
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current.currentTime = 0;
      }
      if (!audioUrl) {
        setIsAudioReady(true);
      }
    }
  }, [audioUrl, videoUrl]);

  useEffect(() => {
    const canPlay = isVideoReady && (isAudioReady || !audioUrl) && videoRef.current;
    if (canPlay) {
      const playMedia = async () => {
        try {
          videoRef.current.volume = videoVolume;
          if (audioRef.current) {
            await Promise.all([
              videoRef.current.play(),
              audioRef.current.play()
            ]);
          } else {
            await videoRef.current.play();
          }
        } catch (error) {
          console.error('Error starting playback:', error);
        }
      };
      playMedia();
    }
  }, [isVideoReady, isAudioReady, videoVolume, audioUrl]);

  useEffect(() => {
    if (currentScene?.story_text) {
      setSubtitleWords(currentScene.story_text.split(' '));
      setVisibleSubtitle(''); // Reset on new scene
    } else {
      setSubtitleWords([]);
      setVisibleSubtitle('');
    }
  }, [currentScene]);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedIdea(initialIdea);
    }, 1200);

    return () => {
      clearTimeout(handler);
    };
  }, [initialIdea]);

  useEffect(() => {
    if (!isMounted.current) {
      isMounted.current = true;
      return;
    }
    const translateIdea = async () => {
      if (language === 'mr' && debouncedIdea.trim()) {
        const hardcodedTranslation = enToMrSuggestionsMap[debouncedIdea.trim().toLowerCase()];
        if (hardcodedTranslation) {
          if (hardcodedTranslation !== initialIdea) {
            setInitialIdea(hardcodedTranslation);
          }
          return; 
        }
        setIsTranslating(true);
        try {
          const response = await fetch(`${API_BASE_URL}/api/translate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: debouncedIdea, target_lang: 'mr' })
          });
          if (!response.ok) {
            const errData = await response.json().catch(() => ({}));
            throw new Error(errData.detail || 'Translation service failed');
          }
          const data = await response.json();
          if (data.translated_text && data.translated_text !== initialIdea) {
            setInitialIdea(data.translated_text);
          }
        } catch (err) {
          console.error("Translation error:", err.message);
        } finally {
          setIsTranslating(false);
        }
      }
    };
    translateIdea();
  }, [debouncedIdea, language]);

  const handlePlaybackChange = (playing) => {
    setIsNarrating(playing);
    setIsPlaying(playing);
  };
  const togglePlayPause = () => {
    if (!videoRef.current) return;
    if (isPlaying) {
      videoRef.current.pause();
      if (audioRef.current) {
        audioRef.current.pause();
      }
    } else {
      videoRef.current.play();
      if (audioRef.current) {
        audioRef.current.play();
      }
    }
  };
  const toggleVideoVolume = () => {
    const newVolume = videoVolume > 0 ? 0 : 0.1;
    setVideoVolume(newVolume);
    if (videoRef.current) {
      videoRef.current.volume = newVolume;
    }
  };
  const replayScene = () => {
    if (videoRef.current) {
      // ======================================================================================
      // *** BEGIN FRONTEND FIX 3/4 ***
      // ======================================================================================
      setHasEnded(false); 
      // ======================================================================================
      // *** END FRONTEND FIX 3/4 ***
      // ======================================================================================
      setIsVideoReady(false);
      setIsAudioReady(false);
      setCurrentTime(0);
      setVisibleSubtitle(''); // Reset visible words
      videoRef.current.currentTime = 0;
      if (audioRef.current) {
        audioRef.current.currentTime = 0;
      }
      if (!audioUrl) {
        setIsAudioReady(true);
      }
    }
  };
  const toggleFullscreen = () => {
    if (!document.fullscreenElement) {
      playerContainerRef.current?.requestFullscreen().catch(err => {
        alert(`Error attempting to enable full-screen mode: ${err.message} (${err.name})`);
      });
    } else {
      document.exitFullscreen();
    }
  };
  const handleSeek = (e) => {
    if (!videoRef.current || isNaN(duration) || duration === 0) return;
    // ======================================================================================
    // *** BEGIN FRONTEND FIX 3/4 (Duplicate) ***
    // ======================================================================================
    setHasEnded(false); 
    // ======================================================================================
    // *** END FRONTEND FIX 3/4 (Duplicate) ***
    // ======================================================================================
    const progressBar = e.currentTarget;
    const clickPosition = e.nativeEvent.offsetX;
    const barWidth = progressBar.clientWidth;
    const seekTime = (clickPosition / barWidth) * duration;
    videoRef.current.currentTime = seekTime;
    if(audioRef.current) {
      audioRef.current.currentTime = seekTime;
    }
    setCurrentTime(seekTime);
  };

  // === NEW: toggleRecording handler ===
  const toggleRecording = async () => {
    if (isRecording) {
      // Stop recording
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      // The 'onstop' event handler will take over
    } else {
      // Start recording
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        
        // Use a high-quality, backend-compatible MIME type
        const mimeType = 'audio/webm;codecs=opus';
        const recorder = new MediaRecorder(stream, { mimeType });
        mediaRecorderRef.current = recorder;
        audioChunksRef.current = [];

        recorder.ondataavailable = (event) => {
          if (event.data.size > 0) {
            audioChunksRef.current.push(event.data);
          }
        };

        recorder.onstop = async () => {
          setIsTranscribing(true);
          const audioBlob = new Blob(audioChunksRef.current, { type: mimeType });
          const formData = new FormData();
          formData.append('file', audioBlob, 'recording.webm');
          
          // Use the specific language codes required by Google STT API
          const sttLanguage = language === 'mr' ? 'mr-IN' : 'en-US';
          formData.append('language', sttLanguage);

          try {
            const response = await fetch(`${API_BASE_URL}/api/transcribe`, {
              method: 'POST',
              body: formData,
            });

            if (!response.ok) {
              const err = await response.json();
              throw new Error(err.detail || 'Transcription failed');
            }

            const data = await response.json();
            if (data.transcript) {
              setInitialIdea(data.transcript); // Set the input field!
            }
          } catch (err) {
            console.error('Transcription error:', err);
            setError(err.message || 'Could not understand audio.');
          } finally {
            setIsTranscribing(false);
            audioChunksRef.current = [];
            // IMPORTANT: Stop the media tracks to turn off the mic light
            stream.getTracks().forEach(track => track.stop());
          }
        };

        recorder.start();
        setIsRecording(true);
      } catch (err) {
        console.error('Error starting recording:', err);
        setError('Microphone access was denied. Please allow microphone access in your browser settings.');
      }
    }
  };
  // === END OF NEW ===

  const executeStartStory = async (prompt) => {
    if (!prompt.trim()) return;
    setLoading(true);
    setError(null);
    setStoryState('loading');
    try {
      const response = await fetch(`${API_BASE_URL}/api/start-story`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          initial_idea: prompt,
          language: language
        })
      });
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Failed to start story`);
      }
      const data = await response.json();
      setSessionId(data.session_id);
      setCurrentScene(data.story_part);
      setVideoUrl(data.video_url);
      setAudioUrl(data.audio_url);
      setStoryState('scene');
    } catch (err) {
      setError(err.message);
      setStoryState('initial');
    } finally {
      setLoading(false);
    }
  };
  const startStory = async () => {
    executeStartStory(initialIdea);
  };
  const handleSuggestionClick = (suggestion) => {
    setInitialIdea(suggestion); 
    executeStartStory(suggestion); 
  };
  const makeChoice = async (choice) => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE_URL}/api/continue-story`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          session_id: sessionId, 
          choice: choice,
          language: language
        })
      });
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Failed to continue story`);
      }
      const data = await response.json();
      setCurrentScene(data.story_part);
      setVideoUrl(data.video_url);
      setAudioUrl(data.audio_url);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };
  const handleFullReset = async () => {
     try {
      await fetch(`${API_BASE_URL}/api/reset`, { 
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: null }) // Resets *all* sessions
      });
      alert('All story sessions have been reset!');
    } catch (err) {
      console.error('Full reset failed:', err);
      alert('Could not reset sessions.');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-100 via-pink-100 to-blue-100 p-4 font-sans">
      <div className="max-w-6xl mx-auto">
        
        <div className="text-center mb-8 pt-8">
          <h1 className="text-5xl font-bold text-purple-600 mb-2 flex items-center justify-center gap-3">
            <SparklesIcon />
            {t.title} 
            <SparklesIcon />
          </h1>
          <p className="text-gray-600 text-lg">{t.subtitle}</p>
        </div>

        {audioUrl && (
          <audio
            ref={audioRef}
            src={`${API_BASE_URL}${audioUrl}`}
            onCanPlayThrough={() => setIsAudioReady(true)}
            onPlay={() => handlePlaybackChange(true)}
            // ======================================================================================
            // *** BEGIN FRONTEND FIX 4/4 ***
            // ======================================================================================
            onEnded={() => {
              handlePlaybackChange(false);
              setHasEnded(true); 
            }}
            // ======================================================================================
            // *** END FRONTEND FIX 4/4 ***
            // ======================================================================================
            onPause={() => handlePlaybackChange(false)}
          />
        )}


        {error && (
          <div className="bg-red-100 border-2 border-red-400 rounded-lg p-4 mb-6">
            <p className="text-red-700 font-semibold">{t.errorPrefix}! {error}</p>
          </div>
        )}

        {storyState === 'initial' && (
          <div className="bg-white rounded-2xl shadow-xl p-8 mb-6">
            
            <div className="flex justify-between items-center mb-4">
                <h2 className="text-2xl font-bold text-gray-800">
                  {t.startTitle}
                </h2>
                <select 
                  value={language} 
                  onChange={(e) => setLanguage(e.target.value)}
                  className="bg-white border-2 border-purple-300 rounded-lg px-3 py-2 text-purple-700 font-medium focus:outline-none focus:border-purple-500"
                >
                  <option value="en">English</option>
                  <option value="mr">मराठी (Marathi)</option>
                </select>
            </div>

            <div className="relative">
              <input
                type="text"
                value={initialIdea}
                onChange={(e) => setInitialIdea(e.target.value)}
                placeholder={t.placeholder}
                // === MODIFIED: Add padding-right for new buttons ===
                className="w-full px-4 py-3 border-2 border-purple-300 rounded-lg mb-4 text-lg focus:outline-none focus:border-purple-500 pr-20"
                onKeyPress={(e) => e.key === 'Enter' && startStory()}
              />
              
              {/* === MODIFIED: Move text translation loader === */}
              {isTranslating && (
                <div className="absolute right-14 top-1/2 -translate-y-1/2" style={{top: '1.1rem'}}>
                  <LoaderIcon className="h-5 w-5 text-purple-400" />
                </div>
              )}

              {/* === NEW: Microphone button === */}
              <div className="absolute right-4 top-1/2 -translate-y-1/2" style={{top: '1.1rem'}}>
                <button
                  type="button"
                  onClick={toggleRecording}
                  disabled={loading || isTranslating} // Disable if starting story or translating text
                  className={`p-1.5 rounded-full flex items-center justify-center transition-all
                    ${isRecording ? 'text-red-500 bg-red-100 hover:bg-red-200' : 'text-purple-500 hover:bg-purple-100'}
                    ${isTranscribing ? 'cursor-not-allowed' : ''}
                  `}
                  title={isRecording ? "Stop Recording" : "Start Recording"}
                >
                  {isTranscribing ? (
                    <LoaderIcon className="h-5 w-5" />
                  ) : isRecording ? (
                    <PauseIcon /> // Using PauseIcon to indicate "stop"
                  ) : (
                    <MicrophoneIcon />
                  )}
                </button>
              </div>
              {/* === END OF NEW === */}

            </div>


            <div className="my-4">
              <p className="text-base text-gray-500 mb-2 text-center">{t.suggestionHeader}</p>
              <div className="flex flex-wrap justify-center gap-2">
                {t.suggestions.map((suggestion) => (
                  <button
                    key={suggestion}
                    onClick={() => handleSuggestionClick(suggestion)}
                    disabled={loading}
                    className="px-6 py-3 bg-purple-50 hover:bg-purple-100 text-purple-600 font-medium rounded-full text-base transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            </div>
            
            <button
              onClick={startStory}
              // === MODIFIED: Disable if recording/transcribing ===
              disabled={!initialIdea.trim() || loading || isTranslating || isRecording || isTranscribing}
              className="w-full bg-gradient-to-r from-purple-500 to-pink-500 text-white font-bold py-3 rounded-lg text-lg hover:from-purple-600 hover:to-pink-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:scale-105 mt-4"
            >
              {/* === MODIFIED: Add new loading states to button text === */}
              {loading ? t.loadingStart : (
                isTranslating ? 'Translating...' : (
                  isRecording ? 'Recording...' : (
                    isTranscribing ? 'Transcribing...' : t.startStory
                  )
                )
              )}
            </button>
            
          </div>
        )}

        
        {storyState === 'loading' && (
          <div className="bg-white rounded-2xl shadow-xl p-12 text-center">
            <div className="text-purple-500 flex justify-center mb-4">
              <LoaderIcon className="h-12 w-12" />
            </div>
            <h3 className="text-2xl font-bold text-gray-800 mb-2">
              {t.loadingScene}
            </h3>
            <p className="text-gray-600">{t.loadingSceneSub}</p>
          </div>
        )}

        {storyState === 'scene' && currentScene && (
          <div className="space-y-6">

            <div className="space-y-6">
            
              {/* --- THIS IS THE UPDATED LINE --- */}
              <div ref={playerContainerRef} className="bg-white rounded-2xl shadow-xl p-6 max-w-3xl mx-auto">
                {videoUrl ? (
                  <div className="relative">
                    <video
                      ref={videoRef}
                      key={videoUrl}
                      loop
                      playsInline
                      className="w-full rounded-lg shadow-lg bg-black cursor-pointer"
                      src={`${API_BASE_URL}${videoUrl}`}
                      onCanPlayThrough={() => setIsVideoReady(true)}
                      onClick={togglePlayPause}
                      onLoadedMetadata={() => setDuration(videoRef.current.duration)}
                      onTimeUpdate={() => {
                        if (!videoRef.current) return;
                        const time = videoRef.current.currentTime;
                        setCurrentTime(time);
                        if (videoRef.current.buffered.length > 0) {
                          setBuffered(videoRef.current.buffered.end(videoRef.current.buffered.length - 1));
                        }
                        if (duration > 0 && subtitleWords.length > 0) {
                          const timePerWord = duration / subtitleWords.length;
                          const wordCountToShow = Math.floor(time / timePerWord) + 1;
                          const visibleWords = subtitleWords.slice(0, wordCountToShow).join(' ');
                          setVisibleSubtitle(visibleWords);
                        }
                      }}
                    />
                    
                    {showSubtitles && currentScene && (
                      <div 
                        className="absolute bottom-16 md:bottom-20 left-1/2 -translate-x-1/2 w-full px-4 pointer-events-none"
                      >
                        <p 
                          className="text-center text-lg md:text-2xl font-semibold text-white"
                          style={{ textShadow: '2px 2px 4px rgba(0, 0, 0, 0.8)' }} 
                        >
                          {visibleSubtitle}
                        </p>
                      </div>
                    )}
                    
                    <div className="absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-black/60 to-transparent">
                      <div 
                        className="relative w-full h-1.5 bg-white/20 rounded-full cursor-pointer"
                        onClick={handleSeek}
                      >
                        <div 
                          className="absolute left-0 top-0 h-full bg-white/40 rounded-full" 
                          style={{ width: `${(buffered / duration) * 100}%` }} 
                        />
                        <div 
                          className="absolute left-0 top-0 h-full bg-pink-500 rounded-full" 
                          style={{ width: `${(currentTime / duration)* 100}%` }} 
                        />
                      </div>
                      
                      <div className="flex justify-between items-center mt-2 text-white">
                        {/* ====================================================================================== */}
                        {/* *** BEGIN FRONTEND FIX (FINAL BUTTON REPLACEMENT) *** */}
                        {/* ====================================================================================== */}
                        <div className="flex gap-2 items-center">
                          <button
                            onClick={hasEnded ? replayScene : togglePlayPause}
                            className="bg-transparent hover:bg-black/70 text-white p-2 rounded-full transition-all"
                            title={isPlaying ? t.titlePause : (hasEnded ? t.replay : t.titlePlay)}
                          >
                            {isPlaying ? <PauseIcon /> : (hasEnded ? <ResetIcon /> : <PlayIcon />)}
                          </button>
                          <button
                            onClick={toggleVideoVolume}
                            className="bg-transparent hover:bg-black/70 text-white p-2 rounded-full transition-all"
                            title={videoVolume > 0 ? t.titleMute : t.titleUnmute}
                          >
                            {videoVolume > 0 ? <VolumeIcon /> : <VolumeMuteIcon />}
                          </button>
                        </div>
                        {/* ====================================================================================== */}
                        {/* *** END FRONTEND FIX (FINAL BUTTON REPLACEMENT) *** */}
                        {/* ====================================================================================== */}
                        
                        <div className="text-sm font-medium">
                          {formatTime(currentTime)} / {formatTime(duration)}
                        </div>
                        
                        <div className="flex gap-2 items-center">
                          <button
                            onClick={() => setShowSubtitles(!showSubtitles)}
                            className={`bg-transparent hover:bg-black/70 p-2 rounded-full transition-all ${
                              showSubtitles ? 'text-pink-400' : 'text-white'
                            }`}
                            title={showSubtitles ? t.titleSubtitlesOn : t.titleSubtitlesOff}
                          >
                            {showSubtitles ? <CCIcon /> : <CCOffIcon />}
                          </button>
                          <button
                            onClick={toggleFullscreen}
                            className="bg-transparent hover:bg-black/70 text-white p-2 rounded-full transition-all"
                            title={isFullscreen ? t.titleFullscreenExit : t.titleFullscreenEnter}
                          >
                            {isFullscreen ? <FullscreenExitIcon /> : <FullscreenEnterIcon />}
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="bg-gray-100 rounded-lg p-12 text-center">
                    <div className="text-gray-400 flex justify-center mb-4">
                      <VideoIcon />
                    </div>
                    <p className="text-gray-600">{t.videoLoading}</p>
                  </div>
                )}
              </div>

              {/* --- THIS IS THE UPDATED LINE --- */}
              <div className="bg-white rounded-2xl shadow-xl p-6 max-w-3xl mx-auto">
                <h3 className="text-xl font-bold text-gray-800 mb-4 text-center">
                  {currentScene.question}
                </h3>
                <div className="space-y-3">
                  {currentScene.choices.map((choice, index) => (
                    <button
                      key={index}
                      onClick={() => makeChoice(choice)}
                      disabled={loading}
                      className="w-full bg-blue-500 hover:bg-blue-600 text-white font-semibold py-4 px-6 rounded-lg text-lg transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed text-center"
                    >
                      {loading ? t.thinking : choice}
                    </button>
                  ))}
                </div>
              </div>

            </div>

            {loading && (
              <div className="bg-white rounded-2xl shadow-xl p-8 text-center">
                <div className="text-purple-500 flex justify-center mb-4">
                  <LoaderIcon className="h-12 w-12" />
                </div>
                <p className="text-lg text-gray-700">{t.loadingNextScene}</p>
              </div>
            )}

          </div>
        )}

      </div>
    </div>
  );
}