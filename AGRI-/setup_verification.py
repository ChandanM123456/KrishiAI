#!/usr/bin/env python3
"""
Setup Verification Script
Verifies that the complete KrishiAI application is properly set up and ready to run
"""

import os
import sys
import subprocess
import warnings
warnings.filterwarnings('ignore')

def check_python_version():
    """Check Python version compatibility"""
    print("Checking Python Version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"  Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"  Python {version.major}.{version.minor}.{version.micro} - NEED 3.8+")
        return False

def check_required_packages():
    """Check if required packages are installed"""
    print("\nChecking Required Packages...")
    
    required_packages = [
        'streamlit',
        'pandas', 
        'numpy',
        'tensorflow',
        'sklearn',
        'PIL',
        'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'PIL':
                import PIL
                print(f"  {package} (Pillow) - OK")
            else:
                __import__(package)
                print(f"  {package} - OK")
        except ImportError:
            print(f"  {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n  Install missing packages: pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_file_structure():
    """Check if all required files exist"""
    print("\nChecking File Structure...")
    
    required_files = [
        'app.py',
        'train_model.py',
        'land_analysis_model.py',
        'requirements.txt',
        'README.md'
    ]
    
    required_dirs = [
        'models',
        'datasets',
        'crop-recommendation-dataset'
    ]
    
    all_good = True
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  {file_path} - OK")
        else:
            print(f"  {file_path} - MISSING")
            all_good = False
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"  {dir_path}/ - OK")
        else:
            print(f"  {dir_path}/ - MISSING")
            all_good = False
    
    return all_good

def check_models():
    """Check if all trained models exist"""
    print("\nChecking Trained Models...")
    
    model_files = [
        'models/land_analysis_cnn.h5',
        'models/crop_recommendation_model.h5', 
        'models/profit_prediction_model.h5',
        'models/weather_optimization_model.h5'
    ]
    
    all_exist = True
    
    for model_file in model_files:
        if os.path.exists(model_file):
            size_mb = os.path.getsize(model_file) / (1024*1024)
            print(f"  {model_file} - OK ({size_mb:.1f} MB)")
        else:
            print(f"  {model_file} - MISSING")
            all_exist = True
    
    if not all_exist:
        print("\n  Run 'python train_model.py' to create missing models")
    
    return all_exist

def check_datasets():
    """Check if datasets exist"""
    print("\nChecking Datasets...")
    
    dataset_files = [
        'crop_data.csv',
        'crop_schedule.csv', 
        'market_data.csv',
        'datasets/land_analysis/labels.csv'
    ]
    
    all_exist = True
    
    for dataset_file in dataset_files:
        if os.path.exists(dataset_file):
            print(f"  {dataset_file} - OK")
        else:
            print(f"  {dataset_file} - MISSING")
            all_exist = False
    
    return all_exist

def check_database():
    """Check database setup"""
    print("\nChecking Database...")
    
    db_file = 'farmers.db'
    if os.path.exists(db_file):
        print(f"  {db_file} - OK")
        return True
    else:
        print(f"  {db_file} - WILL BE CREATED AUTOMATICALLY")
        return True  # Database is created automatically

def test_app_startup():
    """Test if app can start without errors"""
    print("\nTesting App Startup...")
    
    try:
        # Import app to check for syntax errors
        import app
        print("  App syntax - OK")
        
        # Test model loading
        models = app.load_trained_models()
        if models and len(models) == 4:
            print("  Model loading - OK")
        else:
            print("  Model loading - PARTIAL")
        
        return True
        
    except Exception as e:
        print(f"  App startup error: {e}")
        return False

def main():
    """Run complete setup verification"""
    print("="*60)
    print("KRISHIAI SETUP VERIFICATION")
    print("="*60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Required Packages", check_required_packages),
        ("File Structure", check_file_structure),
        ("Trained Models", check_models),
        ("Datasets", check_datasets),
        ("Database", check_database),
        ("App Startup", test_app_startup)
    ]
    
    results = []
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"  {check_name} check ERROR: {e}")
            results.append((check_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("VERIFICATION RESULTS")
    print("="*60)
    
    passed = 0
    total = len(results)
    
    for check_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"  {check_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} checks passed")
    
    if passed == total:
        print("\nSETUP COMPLETE! Application is ready to run.")
        print("\nTo start the application:")
        print("  streamlit run app.py")
        print("\nOr run with specific port:")
        print("  streamlit run app.py --server.port 8501")
    else:
        print(f"\n{total-passed} checks failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("  - Install missing packages: pip install -r requirements.txt")
        print("  - Train models: python train_model.py")
        print("  - Check file permissions")
    
    print("="*60)

if __name__ == "__main__":
    main()
