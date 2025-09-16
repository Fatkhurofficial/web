#!/usr/bin/env python3
"""
Advanced Video Merger dengan Anti-Copyright Protection
Menggabungkan video episode dengan teknik canggih untuk menghindari deteksi copyright
"""

import os
import re
import random
import time
from datetime import datetime, timedelta
import moviepy.editor as mp
from moviepy.editor import VideoFileClip, concatenate_videoclips, ColorClip, CompositeVideoClip
import numpy as np
from pathlib import Path

class AdvancedVideoMerger:
    def __init__(self):
        self.temp_files = []
        self.video_order_log = []
        
    def log(self, message):
        """Print log dengan timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def generate_dynamic_params(self, episode_num, total_episodes):
        """Generate parameter random yang berubah-ubah untuk setiap video"""
        # Seed berdasarkan episode dan waktu untuk randomness yang konsisten tapi berubah
        random.seed(int(time.time()) + episode_num)
        
        # Parameter yang lebih dinamis dan berubah per episode
        base_variation = (episode_num % 10) / 100  # Variasi berdasarkan episode
        time_variation = (int(time.time()) % 1000) / 10000  # Variasi berdasarkan waktu
        
        return {
            'speed': random.uniform(1.001 + base_variation, 1.015 + time_variation),
            'brightness': random.uniform(1.02 + base_variation, 1.12 + time_variation),
            'contrast': random.uniform(0.96 - base_variation, 1.08 + time_variation),
            'saturation': random.uniform(0.94 - base_variation, 1.09 + time_variation),
            'margin': random.randint(2 + (episode_num % 5), 15 + (episode_num % 8)),
            'audio_volume': random.uniform(0.93 + base_variation, 1.08 + time_variation),
            'fade_duration': random.uniform(0.02, 0.08),
            'crop_percent': random.uniform(0.3 + base_variation, 2.5 + time_variation),
            'rotation': random.uniform(-0.8, 0.8),  # Rotasi halus
            'gamma': random.uniform(0.92 + base_variation, 1.1 + time_variation),
            'hue_shift': random.uniform(-5, 5),  # Pergeseran warna
            'noise_level': random.uniform(0.001, 0.008),  # Noise halus
        }
    
    def apply_advanced_color_modifications(self, clip, params, episode_num):
        """Terapkan modifikasi warna yang lebih canggih dan dinamis"""
        try:
            # Brightness
            clip = clip.fx(mp.vfx.colorx, params['brightness'])
            
            # Gamma correction
            clip = clip.fx(mp.vfx.gamma_corr, params['gamma'])
            
            # Hue shift (simulasi dengan color matrix)
            if abs(params['hue_shift']) > 1:
                hue_factor = 1 + (params['hue_shift'] / 100)
                clip = clip.fx(mp.vfx.colorx, hue_factor)
            
            # Dynamic color temperature berdasarkan episode
            if episode_num % 3 == 0:  # Setiap 3 episode
                temp_shift = random.uniform(0.95, 1.05)
                clip = clip.fx(mp.vfx.colorx, temp_shift)
            
        except Exception as e:
            self.log(f"âš ï¸ Warning color modification: {e}")
        
        return clip
    
    def apply_advanced_audio_modifications(self, clip, params):
        """Terapkan modifikasi audio yang canggih"""
        try:
            if clip.audio is None:
                return clip
                
            # Volume adjustment
            clip = clip.volumex(params['audio_volume'])
            
            # Audio fade in/out
            clip = clip.fx(mp.afx.audio_fadein, params['fade_duration'])
            clip = clip.fx(mp.afx.audio_fadeout, params['fade_duration'])
            
            # Subtle speed change yang mempengaruhi pitch
            if random.random() > 0.7:  # 30% chance
                subtle_speed = random.uniform(0.998, 1.002)
                clip = clip.fx(mp.vfx.speedx, subtle_speed)
                
        except Exception as e:
            self.log(f"âš ï¸ Warning audio modification: {e}")
        
        return clip
    
    def apply_advanced_visual_modifications(self, clip, params, episode_num):
        """Terapkan modifikasi visual yang canggih dan dinamis"""
        try:
            # Speed modification yang berbeda per episode
            episode_speed_factor = 1 + ((episode_num % 7) * 0.0002)  # Variasi kecil per episode
            final_speed = params['speed'] * episode_speed_factor
            clip = clip.fx(mp.vfx.speedx, final_speed)
            
            # Margin/border yang berubah
            if params['margin'] > 5:
                clip = clip.margin(params['margin'])
            
            # Dynamic cropping berdasarkan episode
            if params['crop_percent'] > 1.0:
                w, h = clip.size
                crop_factor = 1 - (params['crop_percent']/100)
                crop_w = int(w * crop_factor)
                crop_h = int(h * crop_factor)
                
                # Posisi crop yang berubah per episode
                if episode_num % 4 == 0:  # Center crop
                    x1 = (w - crop_w) // 2
                    y1 = (h - crop_h) // 2
                elif episode_num % 4 == 1:  # Top-left crop
                    x1 = 0
                    y1 = 0
                elif episode_num % 4 == 2:  # Top-right crop
                    x1 = w - crop_w
                    y1 = 0
                else:  # Bottom crop
                    x1 = (w - crop_w) // 2
                    y1 = h - crop_h
                
                clip = clip.crop(x1=x1, y1=y1, x2=x1+crop_w, y2=y1+crop_h)
                clip = clip.resize((w, h))
            
            # Rotasi halus (jika perlu) - skip karena bisa error
            # if abs(params['rotation']) > 0.3:
            #     clip = clip.rotate(params['rotation'])
                
        except Exception as e:
            self.log(f"âš ï¸ Warning visual modification: {e}")
        
        return clip
    
    def add_dynamic_overlay(self, clip, episode_num):
        """Tambahkan overlay yang berubah-ubah per episode"""
        try:
            if random.random() < 0.4:  # 40% chance
                w, h = clip.size
                
                # Overlay yang berbeda berdasarkan episode
                overlay_types = [
                    (0, 0, 0, 3),  # Black
                    (255, 255, 255, 2),  # White
                    (random.randint(10, 50), random.randint(10, 50), random.randint(10, 50), 2),  # Random dark
                ]
                
                overlay_color = overlay_types[episode_num % len(overlay_types)]
                
                overlay = ColorClip(size=(w, h), color=overlay_color[:3], duration=clip.duration)
                overlay = overlay.set_opacity(overlay_color[3] / 255.0)
                
                # Posisi overlay yang berubah
                if episode_num % 5 == 0:
                    overlay = overlay.set_position(('center', 'center'))
                elif episode_num % 5 == 1:
                    overlay = overlay.set_position((0, 0))
                else:
                    overlay = overlay.set_position(('center', 'bottom'))
                
                clip = CompositeVideoClip([clip, overlay])
                
        except Exception as e:
            self.log(f"âš ï¸ Warning overlay: {e}")
        
        return clip
    
    def modify_metadata_advanced(self, output_file):
        """Modifikasi metadata file secara advanced"""
        try:
            # Random timestamp dalam range yang masuk akal
            current_time = time.time()
            random_offset = random.randint(-86400*90, 86400*30)  # -90 hari hingga +30 hari
            new_time = current_time + random_offset
            
            os.utime(output_file, (new_time, new_time))
            self.log(f"âœ… Metadata dimodifikasi: {datetime.fromtimestamp(new_time)}")
            
            # Ubah nama file sementara untuk menghindari pattern detection
            temp_name = f"temp_{random.randint(10000, 99999)}.mp4"
            temp_path = os.path.join(os.path.dirname(output_file), temp_name)
            
            # Tidak perlu rename karena sudah menggunakan timestamp di nama
            
        except Exception as e:
            self.log(f"âš ï¸ Warning metadata: {e}")
    
    def extract_episode_number(self, filename):
        """Extract nomor episode dari filename dengan pattern lebih baik"""
        patterns = [
            r"(?:episode|ep|e)[\s_-]*(\d+)",  # episode 01, ep_01, e-01
            r"s\d+e(\d+)",  # S01E01 format
            r"(\d+)(?:\.mp4|\.avi|\.mkv|\.mov|\.wmv|\.flv)$",  # Angka sebelum ekstensi
            r"(?:^|[^\d])(\d+)(?=[^\d]*$)",  # Angka terakhir dalam nama
        ]
        
        filename_lower = filename.lower()
        for pattern in patterns:
            match = re.search(pattern, filename_lower, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        # Fallback: cari semua angka dan ambil yang paling relevan
        numbers = re.findall(r'\d+', filename)
        if numbers:
            # Ambil angka yang paling masuk akal (biasanya yang terakhir atau terpanjang)
            return int(max(numbers, key=len))
        return 0
    
    def process_single_video(self, filepath, episode_num, total_episodes):
        """Process single video dengan parameter random yang dinamis"""
        self.log(f"ðŸŽ¬ Processing Episode {episode_num}/{total_episodes}: {os.path.basename(filepath)}")
        
        try:
            # Generate parameter dinamis untuk video ini
            params = self.generate_dynamic_params(episode_num, total_episodes)
            
            # Load video
            clip = VideoFileClip(filepath)
            
            # Log informasi video
            duration = clip.duration
            fps = clip.fps if hasattr(clip, 'fps') else 'Unknown'
            self.log(f"   ðŸ“Š Duration: {duration:.1f}s | FPS: {fps} | Size: {clip.size}")
            
            # Apply all modifications
            clip = self.apply_advanced_visual_modifications(clip, params, episode_num)
            clip = self.apply_advanced_color_modifications(clip, params, episode_num)
            clip = self.apply_advanced_audio_modifications(clip, params)
            clip = self.add_dynamic_overlay(clip, episode_num)
            
            # Log parameter yang digunakan
            self.log(f"   ðŸ”§ Speed: {params['speed']:.4f}x | Brightness: {params['brightness']:.3f} | Margin: {params['margin']}px")
            
            # Simpan informasi untuk log
            video_info = {
                'episode': episode_num,
                'filename': os.path.basename(filepath),
                'original_duration': duration,
                'processed_duration': clip.duration,
                'params': params
            }
            self.video_order_log.append(video_info)
            
            return clip
            
        except Exception as e:
            self.log(f"âŒ Error processing {filepath}: {e}")
            return None
    
    def save_order_log(self, folder_path, output_file):
        """Simpan log urutan video ke file txt"""
        folder_name = os.path.basename(os.path.abspath(folder_path))
        log_file = os.path.join(folder_path, f"{folder_name}_merge_log.txt")
        
        try:
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write(f"VIDEO MERGER LOG - {folder_name}\n")
                f.write("=" * 80 + "\n")
                f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Episodes: {len(self.video_order_log)}\n")
                f.write(f"Output File: {os.path.basename(output_file)}\n")
                f.write("=" * 80 + "\n\n")
                
                f.write("URUTAN VIDEO:\n")
                f.write("-" * 80 + "\n")
                
                total_original_duration = 0
                total_processed_duration = 0
                
                for i, video_info in enumerate(self.video_order_log, 1):
                    f.write(f"{i:3d}. Episode {video_info['episode']:3d}: {video_info['filename']}\n")
                    f.write(f"     Original Duration: {video_info['original_duration']:.1f}s\n")
                    f.write(f"     Processed Duration: {video_info['processed_duration']:.1f}s\n")
                    f.write(f"     Speed Modifier: {video_info['params']['speed']:.4f}x\n")
                    f.write(f"     Brightness: {video_info['params']['brightness']:.3f}\n")
                    f.write(f"     Margin: {video_info['params']['margin']}px\n")
                    f.write("-" * 40 + "\n")
                    
                    total_original_duration += video_info['original_duration']
                    total_processed_duration += video_info['processed_duration']
                
                f.write("\nRINGKASAN:\n")
                f.write("-" * 80 + "\n")
                f.write(f"Total Original Duration: {total_original_duration/60:.1f} minutes\n")
                f.write(f"Total Processed Duration: {total_processed_duration/60:.1f} minutes\n")
                f.write(f"Speed Change: {(total_processed_duration/total_original_duration):.4f}x\n")
                f.write(f"Anti-Copyright Features: ACTIVE (Advanced Dynamic)\n")
                f.write("=" * 80 + "\n")
            
            self.log(f"ðŸ“ Log disimpan: {log_file}")
            return log_file
            
        except Exception as e:
            self.log(f"âš ï¸ Warning: Gagal simpan log: {e}")
            return None
    
    def merge_videos(self, folder_path):
        """Main function untuk merge videos dengan logging"""
        folder_name = os.path.basename(os.path.abspath(folder_path))
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(folder_path, f"{folder_name}_merged_{timestamp}.mp4")
        
        self.log(f"ðŸ“ Scanning folder: {folder_path}")
        
        # Find all video files
        video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.m4v']
        all_files = os.listdir(folder_path)
        files = [f for f in all_files if any(f.lower().endswith(ext) for ext in video_extensions)]
        
        if not files:
            self.log("âŒ Tidak ada file video yang ditemukan di folder ini.")
            return
        
        # Sort by episode number
        files.sort(key=self.extract_episode_number)
        total_episodes = len(files)
        
        self.log(f"ðŸ“Š Ditemukan {total_episodes} file video")
        self.log("ðŸ“‹ Urutan episode:")
        for i, f in enumerate(files, 1):
            episode_num = self.extract_episode_number(f)
            file_size = os.path.getsize(os.path.join(folder_path, f)) / (1024*1024)
            self.log(f"   {i:3d}. Episode {episode_num:3d}: {f} ({file_size:.1f} MB)")
        
        # Process each video
        clips = []
        successful_clips = 0
        
        try:
            for i, filename in enumerate(files, 1):
                filepath = os.path.join(folder_path, filename)
                episode_num = self.extract_episode_number(filename)
                
                clip = self.process_single_video(filepath, episode_num, total_episodes)
                if clip is not None:
                    clips.append(clip)
                    successful_clips += 1
                else:
                    self.log(f"âš ï¸ Skipping failed video: {filename}")
        
            if not clips:
                self.log("âŒ Tidak ada video yang berhasil diproses!")
                return
        
            # Concatenate all clips
            self.log(f"ðŸ”— Menggabungkan {successful_clips} video...")
            final_clip = concatenate_videoclips(clips, method="compose")
            
            # Write final video
            self.log(f"ðŸ’¾ Menyimpan video final: {os.path.basename(output_file)}")
            final_clip.write_videofile(
                output_file,
                codec="libx264",
                audio_codec="aac",
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                threads=4,
                preset="medium",
                ffmpeg_params=[
                    "-crf", "23",
                    "-movflags", "+faststart",
                ]
            )
            
            # Clean up clips
            for clip in clips:
                clip.close()
            final_clip.close()
            
            # Modify metadata
            self.modify_metadata_advanced(output_file)
            
            # Save order log
            log_file = self.save_order_log(folder_path, output_file)
            
            # Final stats
            final_size = os.path.getsize(output_file) / (1024*1024)
            total_duration = sum([info['processed_duration'] for info in self.video_order_log])
            
            self.log(f"âœ… SELESAI! Video berhasil digabung")
            self.log(f"ðŸ“ File: {os.path.basename(output_file)}")
            self.log(f"ðŸ“Š Size: {final_size:.1f} MB")
            self.log(f"â±ï¸ Duration: {total_duration/60:.1f} minutes")
            self.log(f"ðŸ›¡ï¸ Anti-copyright: AKTIF (Advanced Dynamic)")
            if log_file:
                self.log(f"ðŸ“ Log file: {os.path.basename(log_file)}")
            
            # Display order summary
            print("\n" + "=" * 60)
            print("ðŸ“‹ RINGKASAN URUTAN VIDEO:")
            print("=" * 60)
            for i, info in enumerate(self.video_order_log, 1):
                print(f"{i:3d}. Episode {info['episode']:3d}: {info['filename']}")
            print("=" * 60)
            
        except Exception as e:
            self.log(f"âŒ Error: {e}")
            # Clean up clips if error
            for clip in clips:
                try:
                    clip.close()
                except:
                    pass

def validate_folder(folder_path):
    """Validasi folder dan tampilkan preview"""
    if not os.path.isdir(folder_path):
        return False, "âŒ Folder tidak ditemukan!"
    
    # Find all video files
    video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.m4v']
    all_files = os.listdir(folder_path)
    video_files = [f for f in all_files if any(f.lower().endswith(ext) for ext in video_extensions)]
    
    if not video_files:
        return False, "âŒ Tidak ada file video ditemukan di folder!"
    
    # Sort by episode
    merger = AdvancedVideoMerger()
    video_files.sort(key=merger.extract_episode_number)
    
    print(f"\nðŸ“ Folder: {folder_path}")
    print(f"ðŸ“Š Ditemukan {len(video_files)} file video:")
    print("-" * 60)
    
    total_size = 0
    total_duration = 0
    
    for i, filename in enumerate(video_files, 1):
        filepath = os.path.join(folder_path, filename)
        try:
            size_mb = os.path.getsize(filepath) / (1024*1024)
            total_size += size_mb
            episode_num = merger.extract_episode_number(filename)
            
            # Coba dapatkan durasi (optional)
            try:
                clip = VideoFileClip(filepath)
                duration = clip.duration
                total_duration += duration
                clip.close()
                duration_str = f" | {duration/60:.1f}min"
            except:
                duration_str = ""
            
            print(f"   {i:2d}. Episode {episode_num:3d}: {filename} ({size_mb:.1f} MB{duration_str})")
            
        except Exception as e:
            print(f"   {i:2d}. Episode ???: {filename} (Error: {e})")
    
    print("-" * 60)
    print(f"ðŸ“Š Total size: {total_size:.1f} MB")
    if total_duration > 0:
        print(f"â±ï¸ Total duration: ~{total_duration/60:.1f} minutes")
    print(f"ðŸ’¾ Estimated output: ~{total_size * 0.9:.1f} MB")
    
    return True, video_files

def main():
    print("=" * 70)
    print("ðŸŽ¬ ADVANCED VIDEO MERGER - Anti Copyright Edition v2.0")
    print("=" * 70)
    print("âœ¨ Fitur Terbaru:")
    print("   â€¢ Parameter dinamis yang berubah per episode")
    print("   â€¢ Logging urutan video ke file txt")
    print("   â€¢ Deteksi episode number yang lebih baik")
    print("   â€¢ Modifikasi visual/audio yang lebih canggih")
    print("   â€¢ Anti-copyright protection berlapis")
    print("   â€¢ Support multiple format video")
    print("   â€¢ Error handling yang lebih baik")
    print("-" * 70)
    
    # Get folder input
    while True:
        folder_input = input("ðŸ“‚ Masukkan path folder yang berisi video: ").strip()
        
        # Remove quotes if present
        folder_input = folder_input.strip('"\'')
        
        if not folder_input:
            print("âŒ Path tidak boleh kosong!")
            continue
            
        # Validate and preview folder
        is_valid, result = validate_folder(folder_input)
        
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
    print("ðŸ›¡ï¸ Mode: Advanced Dynamic Anti-Copyright")
    print("ðŸ“ Log akan disimpan ke file txt")
    confirm = input("ðŸš€ Mulai processing? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("âŒ Processing dibatalkan.")
        return
    
    # Start processing
    print("\n" + "=" * 70)
    print("ðŸš€ MEMULAI PROCESSING...")
    print("=" * 70)
    start_time = time.time()
    
    merger = AdvancedVideoMerger()
    merger.merge_videos(folder_input)
    
    end_time = time.time()
    duration = end_time - start_time
    print(f"â±ï¸ Total waktu processing: {duration/60:.1f} menit")
    print("=" * 70)
    print("ðŸŽ‰ Selamat! Video siap untuk upload!")
    print("ðŸ’¡ Tips: Gunakan title dan description yang unik")
    print("ðŸ“ Cek file log untuk detail urutan episode")
    print("=" * 70)

if __name__ == "__main__":
    main()
