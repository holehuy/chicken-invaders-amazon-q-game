import pygame
import os
import random
import math

class SoundManager:
    def __init__(self):
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Sound effects dictionary
        self.sounds = {}
        
        # Create synthetic sounds
        self._create_sounds()
        
        # Background music
        self.background_music_playing = False
    
    def _create_sounds(self):
        """Create synthetic sound effects since we don't have actual sound files"""
        sounds_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Create shoot sound
        self._create_shoot_sound(os.path.join(sounds_dir, "shoot.wav"))
        
        # Create explosion sound
        self._create_explosion_sound(os.path.join(sounds_dir, "explosion.wav"))
        
        # Create powerup sound
        self._create_powerup_sound(os.path.join(sounds_dir, "powerup.wav"))
        
        # Create hit sound
        self._create_hit_sound(os.path.join(sounds_dir, "hit.wav"))
        
        # Create background music
        self._create_background_music(os.path.join(sounds_dir, "background.wav"))
        
        # Load the created sounds
        self.sounds["shoot"] = pygame.mixer.Sound(os.path.join(sounds_dir, "shoot.wav"))
        self.sounds["explosion"] = pygame.mixer.Sound(os.path.join(sounds_dir, "explosion.wav"))
        self.sounds["powerup"] = pygame.mixer.Sound(os.path.join(sounds_dir, "powerup.wav"))
        self.sounds["hit"] = pygame.mixer.Sound(os.path.join(sounds_dir, "hit.wav"))
        
        # Set volumes
        self.sounds["shoot"].set_volume(0.3)
        self.sounds["explosion"].set_volume(0.5)
        self.sounds["powerup"].set_volume(0.7)
        self.sounds["hit"].set_volume(0.4)
    
    def _create_shoot_sound(self, filename):
        """Create a laser shoot sound effect"""
        pygame.mixer.quit()
        pygame.mixer.init(44100, -16, 1, 1024)
        
        sample_rate = 44100
        duration = 0.2  # seconds
        volume = 0.3
        
        # Create a buffer for the sound
        buffer = bytearray()
        
        # Generate a simple laser sound
        for i in range(int(duration * sample_rate)):
            t = i / sample_rate
            freq = 1000 - 800 * t  # Decreasing frequency
            value = int(volume * 32767 * math.sin(2 * 3.14159 * freq * t))
            
            # Apply envelope
            if t < 0.05:
                # Attack
                value = int(value * (t / 0.05))
            elif t > duration - 0.1:
                # Release
                value = int(value * ((duration - t) / 0.1))
            
            # Convert to 16-bit signed value
            buffer.extend(value.to_bytes(2, byteorder='little', signed=True))
        
        # Save the sound to a file
        with open(filename, 'wb') as f:
            f.write(buffer)
        
        pygame.mixer.quit()
        pygame.mixer.init()
    
    def _create_explosion_sound(self, filename):
        """Create an explosion sound effect"""
        pygame.mixer.quit()
        pygame.mixer.init(44100, -16, 1, 1024)
        
        sample_rate = 44100
        duration = 0.5  # seconds
        volume = 0.5
        
        # Create a buffer for the sound
        buffer = bytearray()
        
        # Generate a noise-based explosion sound
        for i in range(int(duration * sample_rate)):
            t = i / sample_rate
            
            # Mix noise with decreasing frequency
            noise = random.uniform(-1, 1)
            freq = 200 - 180 * t
            tone = math.sin(2 * 3.14159 * freq * t)
            
            # Mix noise and tone
            value = int(volume * 32767 * (0.7 * noise + 0.3 * tone))
            
            # Apply envelope
            if t < 0.05:
                # Attack
                value = int(value * (t / 0.05))
            elif t > duration - 0.2:
                # Release
                value = int(value * ((duration - t) / 0.2))
            
            # Convert to 16-bit signed value
            buffer.extend(value.to_bytes(2, byteorder='little', signed=True))
        
        # Save the sound to a file
        with open(filename, 'wb') as f:
            f.write(buffer)
        
        pygame.mixer.quit()
        pygame.mixer.init()
    
    def _create_powerup_sound(self, filename):
        """Create a power-up collection sound effect"""
        pygame.mixer.quit()
        pygame.mixer.init(44100, -16, 1, 1024)
        
        sample_rate = 44100
        duration = 0.4  # seconds
        volume = 0.7
        
        # Create a buffer for the sound
        buffer = bytearray()
        
        # Generate an ascending tone
        for i in range(int(duration * sample_rate)):
            t = i / sample_rate
            freq = 500 + 1000 * t  # Increasing frequency
            value = int(volume * 32767 * math.sin(2 * 3.14159 * freq * t))
            
            # Apply envelope
            if t < 0.05:
                # Attack
                value = int(value * (t / 0.05))
            elif t > duration - 0.1:
                # Release
                value = int(value * ((duration - t) / 0.1))
            
            # Convert to 16-bit signed value
            buffer.extend(value.to_bytes(2, byteorder='little', signed=True))
        
        # Save the sound to a file
        with open(filename, 'wb') as f:
            f.write(buffer)
        
        pygame.mixer.quit()
        pygame.mixer.init()
    
    def _create_hit_sound(self, filename):
        """Create a hit sound effect"""
        pygame.mixer.quit()
        pygame.mixer.init(44100, -16, 1, 1024)
        
        sample_rate = 44100
        duration = 0.3  # seconds
        volume = 0.4
        
        # Create a buffer for the sound
        buffer = bytearray()
        
        # Generate a hit sound
        for i in range(int(duration * sample_rate)):
            t = i / sample_rate
            
            # Mix noise with decreasing frequency
            noise = random.uniform(-1, 1)
            freq = 300 - 200 * t
            tone = math.sin(2 * 3.14159 * freq * t)
            
            # Mix noise and tone
            value = int(volume * 32767 * (0.5 * noise + 0.5 * tone))
            
            # Apply envelope
            if t < 0.02:
                # Attack
                value = int(value * (t / 0.02))
            elif t > duration - 0.1:
                # Release
                value = int(value * ((duration - t) / 0.1))
            
            # Convert to 16-bit signed value
            buffer.extend(value.to_bytes(2, byteorder='little', signed=True))
        
        # Save the sound to a file
        with open(filename, 'wb') as f:
            f.write(buffer)
        
        pygame.mixer.quit()
        pygame.mixer.init()
    
    def _create_background_music(self, filename):
        """Create a simple background music loop"""
        pygame.mixer.quit()
        pygame.mixer.init(44100, -16, 2, 1024)
        
        sample_rate = 44100
        duration = 10.0  # seconds
        volume = 0.3
        
        # Create a buffer for the sound (stereo)
        buffer = bytearray()
        
        # Base frequencies for a simple chord progression
        chord_progression = [
            [261.63, 329.63, 392.00],  # C major
            [293.66, 349.23, 440.00],  # D minor
            [329.63, 392.00, 493.88],  # E minor
            [349.23, 440.00, 523.25]   # F major
        ]
        
        chord_duration = duration / len(chord_progression)
        
        # Generate a simple background music
        for i in range(int(duration * sample_rate)):
            t = i / sample_rate
            chord_idx = int(t / chord_duration) % len(chord_progression)
            chord = chord_progression[chord_idx]
            
            # Create a simple arpeggio effect
            arp_idx = int(t * 8) % 3
            freq = chord[arp_idx]
            
            # Add some variation
            if int(t * 2) % 2 == 0:
                freq /= 2  # Octave down sometimes
            
            # Generate left and right channel
            left_value = int(volume * 16384 * math.sin(2 * 3.14159 * freq * t))
            
            # Right channel slightly different for stereo effect
            right_value = int(volume * 16384 * math.sin(2 * 3.14159 * (freq * 1.01) * t))
            
            # Apply subtle envelope
            env_mod = 0.8 + 0.2 * math.sin(2 * 3.14159 * 0.5 * t)
            left_value = int(left_value * env_mod)
            right_value = int(right_value * env_mod)
            
            # Convert to 16-bit signed values
            buffer.extend(left_value.to_bytes(2, byteorder='little', signed=True))
            buffer.extend(right_value.to_bytes(2, byteorder='little', signed=True))
        
        # Save the sound to a file
        with open(filename, 'wb') as f:
            f.write(buffer)
        
        pygame.mixer.quit()
        pygame.mixer.init()
    
    def play_sound(self, sound_name):
        """Play a sound effect"""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def play_background_music(self):
        """Start playing background music"""
        if not self.background_music_playing:
            pygame.mixer.music.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "background.wav"))
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)  # Loop indefinitely
            self.background_music_playing = True
    
    def stop_background_music(self):
        """Stop background music"""
        if self.background_music_playing:
            pygame.mixer.music.stop()
            self.background_music_playing = False
