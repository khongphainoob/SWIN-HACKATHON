"""
Interactive API Key Setup Script
Giúp người dùng thiết lập API keys một cách dễ dàng
"""

import os
import sys
from pathlib import Path

def print_header():
    print("\n" + "="*70)
    print("🔑 SWIN AI AGENTIC PROJECT - API KEY SETUP")
    print("="*70 + "\n")

def check_env_file():
    """Kiểm tra và tạo .env file nếu chưa có"""
    env_path = Path(".env")
    env_example_path = Path(".env.example")
    
    if not env_path.exists():
        print("📝 File .env chưa tồn tại.")
        if env_example_path.exists():
            print("   Đang tạo .env từ .env.example...")
            with open(env_example_path, 'r', encoding='utf-8') as src:
                content = src.read()
            with open(env_path, 'w', encoding='utf-8') as dst:
                dst.write(content)
            print("✅ Đã tạo file .env\n")
        else:
            print("❌ Không tìm thấy .env.example")
            return False
    else:
        print("✅ File .env đã tồn tại\n")
    return True

def read_env_file():
    """Đọc file .env và parse thành dict"""
    env_vars = {}
    try:
        with open(".env", 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    except Exception as e:
        print(f"❌ Lỗi đọc .env: {e}")
    return env_vars

def write_env_file(env_vars):
    """Ghi lại file .env với values mới"""
    try:
        lines = []
        with open(".env", 'r', encoding='utf-8') as f:
            for line in f:
                stripped = line.strip()
                if stripped and not stripped.startswith('#') and '=' in stripped:
                    key = stripped.split('=', 1)[0].strip()
                    if key in env_vars:
                        lines.append(f"{key}={env_vars[key]}\n")
                    else:
                        lines.append(line)
                else:
                    lines.append(line)
        
        with open(".env", 'w', encoding='utf-8') as f:
            f.writelines(lines)
        return True
    except Exception as e:
        print(f"❌ Lỗi ghi .env: {e}")
        return False

def get_current_keys():
    """Lấy API keys hiện tại"""
    env_vars = read_env_file()
    
    keys = {
        "OPENAI_API_KEY": env_vars.get("OPENAI_API_KEY", ""),
        "GEMINI_API_KEY": env_vars.get("GEMINI_API_KEY", ""),
        "ANTHROPIC_API_KEY": env_vars.get("ANTHROPIC_API_KEY", ""),
        "GROQ_API_KEY": env_vars.get("GROQ_API_KEY", ""),
    }
    return keys

def display_current_status(keys):
    """Hiển thị trạng thái API keys hiện tại"""
    print("📊 Trạng thái API Keys hiện tại:\n")
    
    status = []
    for provider, key in keys.items():
        provider_name = provider.replace("_API_KEY", "")
        if key and key.strip() and not key.startswith("sk-") and not key.startswith("AIza"):
            # Check if it's just example text
            if key == f"your_{provider_name.lower()}_api_key" or "xxx" in key.lower():
                status.append(f"  ❌ {provider_name:<12} - Chưa có (example value)")
            else:
                status.append(f"  ✅ {provider_name:<12} - Đã có ({len(key)} ký tự)")
        elif key and len(key.strip()) > 10:
            status.append(f"  ✅ {provider_name:<12} - Đã có ({len(key)} ký tự)")
        else:
            status.append(f"  ❌ {provider_name:<12} - Chưa có")
    
    print("\n".join(status))
    print()

def setup_provider_key(provider_name, env_key, current_value):
    """Setup key cho một provider cụ thể"""
    print(f"\n{'='*70}")
    print(f"🔧 Setup {provider_name}")
    print(f"{'='*70}\n")
    
    # Thông tin về provider
    provider_info = {
        "OpenAI": {
            "url": "https://platform.openai.com/api-keys",
            "format": "sk-proj-...",
            "note": "Cần credit card, $5 minimum. GPT-4 best quality.",
            "free": False
        },
        "Gemini": {
            "url": "https://makersuite.google.com/app/apikey",
            "format": "AIzaSy...",
            "note": "Hoàn toàn miễn phí! 60 req/min. Khuyến nghị cho dev.",
            "free": True
        },
        "Anthropic": {
            "url": "https://console.anthropic.com/",
            "format": "sk-ant-...",
            "note": "Claude 3 - chất lượng cao, đắt. $5 minimum.",
            "free": False
        },
        "Groq": {
            "url": "https://console.groq.com/",
            "format": "gsk_...",
            "note": "Cực nhanh, miễn phí beta. Không cần credit card.",
            "free": True
        }
    }
    
    info = provider_info.get(provider_name, {})
    
    if info.get("free"):
        print(f"✅ {provider_name} - MIỄN PHÍ")
    else:
        print(f"💰 {provider_name} - Tốn phí")
    
    print(f"📍 URL: {info.get('url', 'N/A')}")
    print(f"📋 Format: {info.get('format', 'N/A')}")
    print(f"💡 Note: {info.get('note', 'N/A')}\n")
    
    if current_value and len(current_value) > 10 and not "xxx" in current_value.lower():
        print(f"Hiện tại: {current_value[:20]}{'...' if len(current_value) > 20 else ''}")
        choice = input("Giữ nguyên? (y/n) [y]: ").strip().lower()
        if choice != 'n':
            return current_value
    
    new_key = input(f"Nhập {provider_name} API key (Enter để bỏ qua): ").strip()
    
    if new_key:
        # Validate format
        if provider_name == "OpenAI" and not new_key.startswith("sk-"):
            print("⚠️  Warning: OpenAI key thường bắt đầu bằng 'sk-'")
        elif provider_name == "Gemini" and not new_key.startswith("AIza"):
            print("⚠️  Warning: Gemini key thường bắt đầu bằng 'AIza'")
        elif provider_name == "Anthropic" and not new_key.startswith("sk-ant"):
            print("⚠️  Warning: Anthropic key thường bắt đầu bằng 'sk-ant'")
        elif provider_name == "Groq" and not new_key.startswith("gsk_"):
            print("⚠️  Warning: Groq key thường bắt đầu bằng 'gsk_'")
        
        confirm = input("Xác nhận key này? (y/n) [y]: ").strip().lower()
        if confirm != 'n':
            return new_key
    
    return current_value

def interactive_setup():
    """Setup interactive cho all providers"""
    print("🎯 Chọn provider bạn muốn sử dụng:\n")
    print("1. 🧠 Gemini (Google) - MIỄN PHÍ, Khuyến nghị")
    print("2. ⚡ Groq - MIỄN PHÍ, Rất nhanh")
    print("3. 🤖 OpenAI (GPT-4) - Tốn phí, Chất lượng cao")
    print("4. 🎭 Anthropic (Claude) - Tốn phí, Ethical AI")
    print("5. ⚙️  Setup tất cả")
    print("6. ❌ Thoát\n")
    
    choice = input("Chọn (1-6): ").strip()
    
    providers_map = {
        "1": [("Gemini", "GEMINI_API_KEY")],
        "2": [("Groq", "GROQ_API_KEY")],
        "3": [("OpenAI", "OPENAI_API_KEY")],
        "4": [("Anthropic", "ANTHROPIC_API_KEY")],
        "5": [
            ("Gemini", "GEMINI_API_KEY"),
            ("Groq", "GROQ_API_KEY"),
            ("OpenAI", "OPENAI_API_KEY"),
            ("Anthropic", "ANTHROPIC_API_KEY")
        ],
    }
    
    if choice == "6":
        print("\n👋 Thoát setup\n")
        return None
    
    return providers_map.get(choice, [])

def main():
    """Main setup flow"""
    print_header()
    
    # Check .env file
    if not check_env_file():
        print("❌ Không thể tiếp tục. Vui lòng tạo .env file thủ công.")
        return
    
    # Get current keys
    current_keys = get_current_keys()
    display_current_status(current_keys)
    
    # Check if already configured
    has_any_key = any(k and len(k.strip()) > 10 and not "xxx" in k.lower() 
                      for k in current_keys.values())
    
    if has_any_key:
        print("✅ Bạn đã có ít nhất 1 API key được cấu hình.")
        choice = input("Muốn thêm/sửa keys? (y/n) [n]: ").strip().lower()
        if choice != 'y':
            print("\n✅ Setup hoàn tất!\n")
            return
    else:
        print("⚠️  Chưa có API key nào được cấu hình.")
        print("💡 Bạn cần ít nhất 1 API key để chạy hệ thống.\n")
    
    # Interactive setup
    providers_to_setup = interactive_setup()
    
    if providers_to_setup is None:
        return
    
    if not providers_to_setup:
        print("❌ Lựa chọn không hợp lệ")
        return
    
    # Setup each provider
    env_vars = read_env_file()
    updated = False
    
    for provider_name, env_key in providers_to_setup:
        current_value = current_keys.get(env_key, "")
        new_value = setup_provider_key(provider_name, env_key, current_value)
        
        if new_value != current_value:
            env_vars[env_key] = new_value
            updated = True
            print(f"✅ {provider_name} key đã được cập nhật\n")
    
    # Save to .env
    if updated:
        if write_env_file(env_vars):
            print("\n" + "="*70)
            print("✅ ĐÃ LƯU CẤU HÌNH VÀO .env")
            print("="*70 + "\n")
        else:
            print("❌ Có lỗi khi lưu file .env")
            return
    else:
        print("\n⚠️  Không có thay đổi nào được lưu\n")
    
    # Final status
    print("📊 Trạng thái cuối cùng:\n")
    final_keys = get_current_keys()
    display_current_status(final_keys)
    
    # Next steps
    print("\n" + "="*70)
    print("🎯 BƯỚC TIẾP THEO")
    print("="*70 + "\n")
    print("1. Test API keys:")
    print("   python test_streamlit_ready.py\n")
    print("2. Chạy workflow test:")
    print("   python test_workflow_quick.py\n")
    print("3. Khởi động Streamlit app:")
    print("   .\\start_streamlit.ps1\n")
    print("📚 Xem thêm: API_SETUP_GUIDE.md\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Setup bị hủy bởi người dùng\n")
    except Exception as e:
        print(f"\n❌ Lỗi: {e}\n")
        import traceback
        traceback.print_exc()
