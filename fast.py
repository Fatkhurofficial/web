#!/usr/bin/env python3
"""
Advanced Video Merger - FAST VERSION
Optimized untuk kecepatan processing dengan parallel processing dan optimized settings
"""

import os
import re
import random
import time
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing
import psutil

# Fix untuk PIL/Pillow compatibility
try:
    from PIL import Image
    if not hasattr(Image, 'ANTIALIAS'):
        Image.ANTIALIAS = Image.LANCZOS
    if not hasattr(Image, 'CUBIC'):
        Image.CUBIC = Image.BICUBIC
except ImportError:
    pass

import moviepy.editor as mp
from moviepy.editor import VideoFileClip, concatenate_videoclips, ColorClip, CompositeVideoClip
import numpy as np
from pathlib import Path

class FastVideoMerger:
    def __init__(self, speed_mode="balanced"):
        self.temp_files = []
        self.video_order_log = []
        self.speed_mode = speed_mode  # "ultrafast", "fast", "balanced", "quality"
        self.cpu_count = min(multiprocessing.cpu_count(), 8)  # Max 8 cores
        self.available_memory = psutil.virtual_memory().available / (1024**3)  # GB
        
        # Speed presets
        self.presets = {
            'ultrafast': {
                'ffmpeg_preset': 'ultrafast',
                'crf': 28,
                'threads': self.cpu_count,
                'enable_overlay': False,
                'enable_complex_effects': False,
                'batch_size': 20,
                'parallel_processing': True
            },
            'fast': {
                'ffmpeg_preset': 'fast', 
                'crf': 25,
                'threads': max(4, self.cpu_count // 2),
                'enable_overlay': False,
                'enable_complex_effects': True,
                'batch_size': 15,
                'parallel_processing': True
            },
            'balanced': {
                'ffmpeg_preset': 'medium',
                'crf': 23,
                'threads': max(4, self.cpu_count // 2),
                'enable_overlay': True,
                'enable_complex_effects': True,
                'batch_size': 10,
                'parallel_processing': True
            },
            'quality': {
                'ffmpeg_preset': 'slow',
                'crf': 20,
                'threads': max(2, self.cpu_count // 4),
                'enable_overlay': True,
                'enable_complex_effects': True,
                'batch_size': 5,
                'parallel_processing': False
            }
        }
        
        self.config = self.presets[speed_mode]
        self.log(f"ðŸš€ FastVideoMerger initialized - Mode: {speed_mode.upper()}")
        self.log(f"ðŸ’» CPU Cores: {self.cpu_count} | Available RAM: {self.available_memory:.1f}GB")
        
    def log(self, message):
        """Print log dengan timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def generate_optimized_params(self, episode_num, total_episodes):
        """Generate parameter yang dioptimasi untuk kecepatan"""
        random.seed(int(time.time()) + episode_num)
        
        base_variation = (episode_num % 10) / 100
        time_variation = (int(time.time()) % 1000) / 10000
        
        if self.speed_mode == "ultrafast":
            # Minimal processing untuk ultrafast
            return {
                'speed': random.uniform(1.001, 1.008),  # Minimal speed change
                'brightness': random.uniform(1.01, 1.05),  # Subtle brightness
                'margin': random.randint(2, 8),  # Small margins
                'audio_volume': random.uniform(0.98, 1.02),  # Minimal audio change
                'fade_duration': 0.01,  # Minimal fade
                'crop_percent': 0,  # No cropping for speed
            }
        elif self.speed_mode == "fast":
            return {
                'speed': random.uniform(1.001, 1.012),
                'brightness': random.uniform(1.02, 1.08), 
                'margin': random.randint(3, 10),
                'audio_volume': random.uniform(0.95, 1.05),
                'fade_duration': random.uniform(0.01, 0.03),
                'crop_percent': random.uniform(0, 1.0),
            }
        else:
            # Full parameters untuk balanced/quality
            return {
                'speed': random.uniform(1.001 + base_variation, 1.015 + time_variation),
                'brightness': random.uniform(1.02 + base_variation, 1.12 + time_variation),
                'contrast': random.uniform(0.96 - base_variation, 1.08 + time_variation),
                'saturation': random.uniform(0.94 - base_variation, 1.09 + time_variation),
                'margin': random.randint(2 + (episode_num % 5), 15 + (episode_num % 8)),
                'audio_volume': random.uniform(0.93 + base_variation, 1.08 + time_variation),
                'fade_duration': random.uniform(0.02, 0.08),
                'crop_percent': random.uniform(0.3 + base_variation, 2.5 + time_variation),
                'gamma': random.uniform(0.92 + base_variation, 1.1 + time_variation),
            }
    
    def apply_fast_modifications(self, clip, params, episode_num):
        """Apply modifications dengan optimasi kecepatan"""
        try:
            # Speed modification (always applied)
            if params['speed'] != 1.0:
                clip = clip.fx(mp.vfx.speedx, params['speed'])
            
            # Brightness (lightweight)
            if params['brightness'] != 1.0:
                clip = clip.fx(mp.vfx.colorx, params['brightness'])
            
            # Margin (if not ultrafast)
            if self.speed_mode != "ultrafast" and params.get('margin', 0) > 5:
                clip = clip.margin(params['margin'])
            
            # Advanced effects only for balanced/quality modes
            if self.config['enable_complex_effects']:
                # Gamma correction
                if params.get('gamma') and abs(params['gamma'] - 1.0) > 0.05:
                    clip = clip.fx(mp.vfx.gamma_corr, params['gamma'])
                
                # Cropping (expensive operation)
                if params.get('crop_percent', 0) > 1.0:
                    w, h = clip.size
                    crop_factor = 1 - (params['crop_percent']/100)
                    crop_w = int(w * crop_factor)
                    crop_h = int(h * crop_factor)
                    
                    x1 = (w - crop_w) // 2
                    y1 = (h - crop_h) // 2
                    
                    clip = clip.crop(x1=x1, y1=y1, x2=x1+crop_w, y2=y1+crop_h)
                    clip = clip.resize((w, h))
            
        except Exception as e:
            self.log(f"âš ï¸ Warning modification: {e}")
        
        return clip
    
    def apply_fast_audio_modifications(self, clip, params):
        """Apply audio modifications dengan optimasi"""
        try:
            if clip.audio is None:
                return clip
                
            # Volume (always applied)
            if params['audio_volume'] != 1.0:
                clip = clip.volumex(params['audio_volume'])
            
            # Fade (minimal for speed)
            if params.get('fade_duration', 0) > 0.005:
                clip = clip.fx(mp.afx.audio_fadein, params['fade_duration'])
                clip = clip.fx(mp.afx.audio_fadeout, params['fade_duration'])
                
        except Exception as e:
            self.log(f"âš ï¸ Warning audio: {e}")
        
        return clip
    
    def add_fast_overlay(self, clip, episode_num):
        """Add overlay hanya jika diaktifkan"""
        if not self.config['enable_overlay']:
            return clip
            
        try:
            if random.random() < 0.2:  # 20% chance, reduced from 40%
                w, h = clip.size
                overlay_color = (random.randint(0, 30), random.randint(0, 30), random.randint(0, 30), 1)
                overlay = ColorClip(size=(w, h), color=overlay_color[:3], duration=clip.duration)
                overlay = overlay.set_opacity(overlay_color[3] / 255.0)
                clip = CompositeVideoClip([clip, overlay])
                
        except Exception as e:
            self.log(f"âš ï¸ Warning overlay: {e}")
        
        return clip

    def process_single_video_fast(self, args):
        """Process single video dengan optimasi untuk parallel processing"""
        filepath, episode_num, total_episodes = args
        
        try:
            # Generate parameter
            params = self.generate_optimized_params(episode_num, total_episodes)
            
            # Load video dengan timeout
            clip = VideoFileClip(filepath, verbose=False)
            
            # Apply modifications
            clip = self.apply_fast_modifications(clip, params, episode_num)
            clip = self.apply_fast_audio_modifications(clip, params)
            
            if self.config['enable_overlay']:
                clip = self.add_fast_overlay(clip, episode_num)
            
            # Store info for logging
            video_info = {
                'episode': episode_num,
                'filename': os.path.basename(filepath),
                'original_duration': clip.duration if hasattr(clip, 'duration') else 0,
                'processed_duration': clip.duration,
                'params': params
            }
            
            return clip, video_info
            
        except Exception as e:
            self.log(f"âŒ Error processing {filepath}: {e}")
            return None, None
    
    def extract_episode_number(self, filename):
        """Extract nomor episode dengan pattern matching yang optimized"""
        patterns = [
            r"(?:episode|ep|e)[\s_-]*(\d+)",
            r"s\d+e(\d+)",
            r"(\d+)(?:\.mp4|\.avi|\.mkv|\.mov|\.wmv|\.flv)$",
            r"(?:^|[^\d])(\d+)(?=[^\d]*$)",
        ]
        
        filename_lower = filename.lower()
        for pattern in patterns:
            match = re.search(pattern, filename_lower, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        numbers = re.findall(r'\d+', filename)
        if numbers:
            return int(max(numbers, key=len))
        return 0
    
    def batch_process_videos(self, file_paths_with_info):
        """Process videos dalam batch untuk memory management"""
        processed_clips = []
        total_files = len(file_paths_with_info)
        batch_size = self.config['batch_size']
        
        for i in range(0, total_files, batch_size):
            batch = file_paths_with_info[i:i + batch_size]
            batch_num = (i // batch_size) + 1
            total_batches = (total_files + batch_size - 1) // batch_size
            
            self.log(f"ðŸ”„ Processing batch {batch_num}/{total_batches} ({len(batch)} videos)")
            
            # Process batch
            if self.config['parallel_processing'] and len(batch) > 1:
                # Parallel processing
                max_workers = min(len(batch), max(2, self.cpu_count // 2))
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    results = list(executor.map(self.process_single_video_fast, batch))
            else:
                # Sequential processing
                results = [self.process_single_video_fast(args) for args in batch]
            
            # Collect results
            for clip, video_info in results:
                if clip is not None and video_info is not None:
                    processed_clips.append(clip)
                    self.video_order_log.append(video_info)
                    self.log(f"   âœ… Episode {video_info['episode']}: {video_info['filename']}")
            
            # Memory cleanup setiap batch
            if i + batch_size < total_files:
                self.log(f"   ðŸ§¹ Memory cleanup after batch {batch_num}")
                # Force garbage collection jika perlu
                import gc
                gc.collect()
        
        return processed_clips
    
    def get_optimized_ffmpeg_params(self):
        """Get FFmpeg parameters yang dioptimasi berdasarkan mode"""
        base_params = [
            "-c:v", "libx264",
            "-preset", self.config['ffmpeg_preset'],
            "-crf", str(self.config['crf']),
            "-movflags", "+faststart",
        ]
        
        # Hardware acceleration jika tersedia
        if self.speed_mode in ["ultrafast", "fast"]:
            base_params.extend([
                "-tune", "fastdecode",
                "-x264opts", "no-scenecut",  # Disable scene cut analysis
            ])
        
        # Threading
        base_params.extend(["-threads", str(self.config['threads'])])
        
        return base_params
    
    def save_order_log_fast(self, folder_path, output_file):
        """Save log dengan format yang optimized"""
        folder_name = os.path.basename(os.path.abspath(folder_path))
        log_file = os.path.join(folder_path, f"{folder_name}_merge_log_fast.txt")
        
        try:
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write(f"FAST VIDEO MERGER LOG - {folder_name}\n")
                f.write("=" * 80 + "\n")
                f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Speed Mode: {self.speed_mode.upper()}\n")
                f.write(f"Total Episodes: {len(self.video_order_log)}\n")
                f.write(f"CPU Cores Used: {self.config['threads']}\n")
                f.write(f"Parallel Processing: {'ON' if self.config['parallel_processing'] else 'OFF'}\n")
                f.write(f"Output File: {os.path.basename(output_file)}\n")
                f.write("=" * 80 + "\n\n")
                
                f.write("URUTAN VIDEO:\n")
                f.write("-" * 80 + "\n")
                
                total_original_duration = 0
                total_processed_duration = 0
                
                for i, video_info in enumerate(self.video_order_log, 1):
                    f.write(f"{i:3d}. Episode {video_info['episode']:3d}: {video_info['filename']}\n")
                    f.write(f"     Duration: {video_info['processed_duration']:.1f}s\n")
                    f.write(f"     Speed: {video_info['params']['speed']:.4f}x\n")
                    if i % 10 == 0:  # Add separator every 10 episodes
                        f.write("-" * 40 + "\n")
                    
                    total_processed_duration += video_info['processed_duration']
                
                f.write(f"\nTOTAL DURATION: {total_processed_duration/60:.1f} minutes\n")
                f.write(f"OPTIMIZATION: {self.speed_mode.upper()} mode\n")
                f.write("=" * 80 + "\n")
            
            self.log(f"ðŸ“ Fast log saved: {log_file}")
            return log_file
            
        except Exception as e:
            self.log(f"âš ï¸ Warning: Gagal simpan log: {e}")
            return None
    
    def merge_videos_fast(self, folder_path):
        """Main function untuk fast merge dengan semua optimasi"""
        folder_name = os.path.basename(os.path.abspath(folder_path))
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(folder_path, f"{folder_name}_merged_fast_{timestamp}.mp4")
        
        self.log(f"ðŸ“ Fast processing folder: {folder_path}")
        
        # Find video files
        video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.m4v']
        all_files = os.listdir(folder_path)
        files = [f for f in all_files if any(f.lower().endswith(ext) for ext in video_extensions)]
        
        if not files:
            self.log("âŒ Tidak ada file video yang ditemukan!")
            return
        
        # Sort by episode number
        files.sort(key=self.extract_episode_number)
        total_episodes = len(files)
        
        self.log(f"ðŸ“Š Ditemukan {total_episodes} video files")
        self.log(f"âš¡ Speed mode: {self.speed_mode.upper()}")
        self.log(f"ðŸ”§ Parallel processing: {'ON' if self.config['parallel_processing'] else 'OFF'}")
        self.log(f"ðŸ’¾ Batch size: {self.config['batch_size']}")
        
        # Prepare file info for batch processing
        file_paths_with_info = []
        for filename in files:
            filepath = os.path.join(folder_path, filename)
            episode_num = self.extract_episode_number(filename)
            file_paths_with_info.append((filepath, episode_num, total_episodes))
        
        start_time = time.time()
        
        try:
            # Batch process videos
            clips = self.batch_process_videos(file_paths_with_info)
            
            if not clips:
                self.log("âŒ Tidak ada video yang berhasil diproses!")
                return
            
            processing_time = time.time() - start_time
            self.log(f"â±ï¸ Processing time: {processing_time:.1f} seconds")
            self.log(f"ðŸ”— Concatenating {len(clips)} videos...")
            
            # Concatenate with optimized method
            concat_start = time.time()
            final_clip = concatenate_videoclips(clips, method="compose")
            concat_time = time.time() - concat_start
            self.log(f"â±ï¸ Concatenation time: {concat_time:.1f} seconds")
            
            # Write final video dengan optimized settings
            self.log(f"ðŸ’¾ Writing final video: {os.path.basename(output_file)}")
            write_start = time.time()
            
            final_clip.write_videofile(
                output_file,
                codec="libx264",
                audio_codec="aac",
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                threads=self.config['threads'],
                preset=self.config['ffmpeg_preset'],
                verbose=False,
                ffmpeg_params=self.get_optimized_ffmpeg_params()
            )
            
            write_time = time.time() - write_start
            total_time = time.time() - start_time
            
            # Cleanup
            for clip in clips:
                clip.close()
            final_clip.close()
            
            # Save log
            log_file = self.save_order_log_fast(folder_path, output_file)
            
            # Final stats
            final_size = os.path.getsize(output_file) / (1024*1024)
            total_duration = sum([info['processed_duration'] for info in self.video_order_log])
            
            self.log(f"âœ… FAST MERGE COMPLETED!")
            self.log(f"ðŸ“ File: {os.path.basename(output_file)}")
            self.log(f"ðŸ“Š Size: {final_size:.1f} MB")
            self.log(f"â±ï¸ Duration: {total_duration/60:.1f} minutes")
            self.log(f"ðŸš€ Total time: {total_time:.1f} seconds")
            self.log(f"âš¡ Speed: {total_duration/total_time:.1f}x realtime")
            self.log(f"ðŸ›¡ï¸ Anti-copyright: ACTIVE ({self.speed_mode.upper()} mode)")
            
            # Performance summary
            print("\n" + "=" * 70)
            print("âš¡ PERFORMANCE SUMMARY:")
            print("=" * 70)
            print(f"Processing: {processing_time:.1f}s | Concat: {concat_time:.1f}s | Write: {write_time:.1f}s")
            print(f"Total: {total_time:.1f}s | Speed: {total_duration/total_time:.1f}x realtime")
            print(f"Throughput: {len(clips)/total_time:.2f} videos/second")
            print("=" * 70)
            
        except Exception as e:
            self.log(f"âŒ Error: {e}")
            # Cleanup on error
            for clip in clips if 'clips' in locals() else []:
                try:
                    clip.close()
                except:
                    pass

def select_speed_mode():
    """Interface untuk memilih speed mode"""
    print("\nðŸš€ PILIH SPEED MODE:")
    print("=" * 50)
    print("1. ULTRAFAST - Tercepat, kualitas standar")
    print("   â€¢ FFmpeg: ultrafast preset")
    print("   â€¢ CRF: 28 (file lebih kecil)")  
    print("   â€¢ Effects: Minimal")
    print("   â€¢ Best for: 50+ episodes, butuh cepat")
    print()
    print("2. FAST - Cepat dengan kualitas bagus")
    print("   â€¢ FFmpeg: fast preset")
    print("   â€¢ CRF: 25 (balanced)")
    print("   â€¢ Effects: Sebagian")
    print("   â€¢ Best for: 20-50 episodes")
    print()
    print("3. BALANCED - Seimbang speed vs quality")
    print("   â€¢ FFmpeg: medium preset")
    print("   â€¢ CRF: 23 (good quality)")
    print("   â€¢ Effects: Semua")
    print("   â€¢ Best for: 10-30 episodes")
    print()
    print("4. QUALITY - Kualitas terbaik (lambat)")
    print("   â€¢ FFmpeg: slow preset")
    print("   â€¢ CRF: 20 (high quality)")
    print("   â€¢ Effects: Semua + advanced")
    print("   â€¢ Best for: <15 episodes")
    print("-" * 50)
    
    while True:
        choice = input("Pilih mode (1-4): ").strip()
        if choice == "1":
            return "ultrafast"
        elif choice == "2":
            return "fast"
        elif choice == "3":
            return "balanced"
        elif choice == "4":
            return "quality"
        else:
            print("âŒ Pilihan tidak valid! Masukkan 1-4")

def validate_folder_fast(folder_path):
    """Validasi folder dengan preview yang optimized"""
    if not os.path.isdir(folder_path):
        return False, "âŒ Folder tidak ditemukan!"
    
    video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.m4v']
    all_files = os.listdir(folder_path)
    video_files = [f for f in all_files if any(f.lower().endswith(ext) for ext in video_extensions)]
    
    if not video_files:
        return False, "âŒ Tidak ada file video ditemukan!"
    
    merger = FastVideoMerger()
    video_files.sort(key=merger.extract_episode_number)
    
    print(f"\nðŸ“ Folder: {folder_path}")
    print(f"ðŸ“Š Ditemukan {len(video_files)} file video:")
    print("-" * 60)
    
    total_size = 0
    sample_count = min(10, len(video_files))  # Show max 10 for speed
    
    for i, filename in enumerate(video_files[:sample_count], 1):
        filepath = os.path.join(folder_path, filename)
        try:
            size_mb = os.path.getsize(filepath) / (1024*1024)
            total_size += size_mb
            episode_num = merger.extract_episode_number(filename)
            print(f"   {i:2d}. Episode {episode_num:3d}: {filename} ({size_mb:.1f} MB)")
        except:
            print(f"   {i:2d}. Episode ???: {filename} (Error reading)")
    
    if len(video_files) > sample_count:
        print(f"   ... dan {len(video_files) - sample_count} file lainnya")
        # Estimate total size
        avg_size = total_size / sample_count
        total_size = avg_size * len(video_files)
    
    print("-" * 60)
    print(f"ðŸ“Š Estimated total size: ~{total_size:.1f} MB")
    print(f"ðŸ’¾ Estimated output: ~{total_size * 0.85:.1f} MB")
    
    return True, video_files

def main():
    print("=" * 70)
    print("ðŸš€ ADVANCED VIDEO MERGER - FAST VERSION")
    print("=" * 70)
    print("âš¡ Features:")
    print("   â€¢ Parallel processing untuk kecepatan maksimal")
    print("   â€¢ Multiple speed modes (ultrafast to quality)")
    print("   â€¢ Hardware-optimized FFmpeg settings")
    print("   â€¢ Batch processing untuk memory efficiency")
    print("   â€¢ Real-time performance monitoring")
    print("   â€¢ Anti-copyright protection tetap aktif")
    print("-" * 70)
    
    # Select speed mode
    speed_mode = select_speed_mode()
    
    # Get folder input
    while True:
        folder_input = input("\nðŸ“‚ Masukkan path folder video: ").strip().strip('"\'')
        
        if not folder_input:
            print("âŒ Path tidak boleh kosong!")
            continue
            
        is_valid, result = validate_folder_fast(folder_input)
        
        if not is_valid:
            print(result)
            retry = input("ðŸ”„ Coba lagi? (y/n): ").strip().lower()
            if retry != 'y':
                print("âŒ Program dibatalkan.")
                return
            continue
        else:
            break
    
    # Confirm processing
    print(f"\nðŸŽ¯ Folder target: {folder_input}")
    print(f"âš¡ Speed mode: {speed_mode.upper()}")
    print("ðŸ›¡ï¸ Anti-copyright: ACTIVE")
    
    # Show expected performance
    file_count = len(result)
    if speed_mode == "ultrafast":
        est_time = file_count * 0.1  # ~0.1 seconds per file
    elif speed_mode == "fast":
        est_time = file_count * 0.2
    elif speed_mode == "balanced":
        est_time = file_count * 0.5
    else:
        est_time = file_count * 1.0
    
    print(f"â±ï¸ Estimated processing time: ~{est_time:.1f} seconds")
    
    confirm = input("ðŸš€ Mulai fast processing? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("âŒ Processing dibatalkan.")
        return
    
    # Start processing
    print("\n" + "=" * 70)
    print("ðŸš€ STARTING FAST PROCESSING...")
    print("=" * 70)
    
    merger = FastVideoMerger(speed_mode)
    merger.merge_videos_fast(folder_input)
    
    print("=" * 70)
    print("ðŸŽ‰ FAST PROCESSING COMPLETED!")
    print("ðŸ’¡ Tips: File sudah dioptimasi untuk upload cepat!")
    print("=" * 70)

if __name__ == "__main__":
    main()
