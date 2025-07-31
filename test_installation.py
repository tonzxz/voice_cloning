#!/usr/bin/env python3
"""
Installation Test Script for Geria Voice Cloning
Tests if all required dependencies are properly installed
"""

import sys
import importlib

def test_import(module_name, package_name=None):
    """Test if a module can be imported"""
    try:
        importlib.import_module(module_name)
        print(f"✅ {package_name or module_name}")
        return True
    except ImportError as e:
        print(f"❌ {package_name or module_name}: {e}")
        return False

def main():
    print("🧪 Testing Geria Voice Cloning Dependencies...\n")
    
    # Check Python version
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"🐍 Python Version: {python_version}")
    
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ is required")
        return False
    else:
        print("✅ Python version is compatible\n")
    
    # Test core dependencies
    print("📦 Testing Core Dependencies:")
    dependencies = [
        ("streamlit", "Streamlit"),
        ("TTS", "Coqui TTS"),
        ("torch", "PyTorch"),
        ("torchaudio", "TorchAudio"),
        ("librosa", "Librosa"),
        ("soundfile", "SoundFile"),
        ("numpy", "NumPy"),
        ("scipy", "SciPy"),
        ("pydub", "PyDub"),
        ("omegaconf", "OmegaConf"),
        ("pathlib", "Pathlib"),
        ("requests", "Requests"),
    ]
    
    all_passed = True
    for module, name in dependencies:
        if not test_import(module, name):
            all_passed = False
    
    print("\n📝 Testing Text Processing:")
    text_deps = [
        ("inflect", "Inflect"),
        ("pypinyin", "PyPinyin"),
        ("jieba", "Jieba"),
        ("jamo", "Jamo"),
        ("gruut", "Gruut"),
        ("phonemizer", "Phonemizer"),
    ]
    
    for module, name in text_deps:
        test_import(module, name)
    
    print(f"\n{'🎉 All tests passed!' if all_passed else '❌ Some dependencies failed'}")
    
    if all_passed:
        print("\n🚀 Ready to run: python -m streamlit run app.py")
    else:
        print("\n🔧 Please run setup.sh (Linux/Mac) or setup.bat (Windows) to fix issues")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
