import torch

class AudioDurationCalculator:
    """
    Node simplu pentru calcularea duratei audio și frame count
    Input: AUDIO object din alt LoadAudio node
    Output: duration (INT), frame_count (INT)
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "audio": ("AUDIO",),
                "fps": ("FLOAT", {
                    "default": 30.0,
                    "min": 1.0,
                    "max": 120.0,
                    "step": 0.1,
                    "display": "number"
                }),
            }
        }
    
    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("audio_duration_seconds", "frame_count")
    FUNCTION = "calculate"
    CATEGORY = "audio/analysis"

    def validate_audio_input(self, audio):
        """Validează formatul audio input"""
        if not isinstance(audio, dict) or 'waveform' not in audio or 'sample_rate' not in audio:
            raise ValueError("Expected audio input to be a dictionary with 'waveform' and 'sample_rate' keys")

    def get_audio_duration(self, audio):
        """Calculează durata audio în secunde"""
        if isinstance(audio, dict) and 'waveform' in audio and 'sample_rate' in audio:
            return audio['waveform'].shape[-1] / audio['sample_rate']
        else:
            raise ValueError("Invalid audio input format")

    def calculate(self, audio, fps):
        try:
            # Validează input-ul
            self.validate_audio_input(audio)
            
            # Calculează durata în secunde
            duration_seconds = self.get_audio_duration(audio)
            
            # Calculează frame count = duration * fps
            frame_count = int(duration_seconds * fps)
            
            # Return duration ca INT (rotunjit)
            duration_int = int(round(duration_seconds))
            
            return (duration_int, frame_count)
            
        except Exception as e:
            print(f"AudioDurationCalculator error: {str(e)}")
            return (0, 0)

# Mapare pentru ComfyUI
NODE_CLASS_MAPPINGS = {
    "AudioDurationCalculator": AudioDurationCalculator,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AudioDurationCalculator": "Audio Duration Calculator",
}