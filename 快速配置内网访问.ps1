# ========================================
# 初中学习系统 - 内网访问快速配置脚本
# ========================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  初中学习系统 - 内网访问配置向导" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. 检测内网IP
Write-Host "步骤1：检测服务器内网IP..." -ForegroundColor Yellow
$networkAdapters = Get-NetIPAddress -AddressFamily IPv4 | Where-Object {
    $_.InterfaceAlias -notlike "*Loopback*" -and 
    $_.IPAddress -notlike "169.254.*"
}

if ($networkAdapters.Count -eq 0) {
    Write-Host "❌ 未检测到有效的内网IP地址" -ForegroundColor Red
    exit
}

Write-Host ""
Write-Host "检测到以下网络接口：" -ForegroundColor Green
$i = 1
foreach ($adapter in $networkAdapters) {
    Write-Host "  [$i] $($adapter.InterfaceAlias): $($adapter.IPAddress)" -ForegroundColor Cyan
    $i++
}

Write-Host ""
if ($networkAdapters.Count -eq 1) {
    $selectedIP = $networkAdapters[0].IPAddress
    Write-Host "自动选择IP: $selectedIP" -ForegroundColor Green
} else {
    $selection = Read-Host "请选择要使用的网络接口编号 (1-$($networkAdapters.Count))"
    $selectedIP = $networkAdapters[$selection - 1].IPAddress
    Write-Host "已选择IP: $selectedIP" -ForegroundColor Green
}

Write-Host ""

# 2. 更新.env文件
Write-Host "步骤2：更新Django配置..." -ForegroundColor Yellow

$envPath = "study\.env"

if (Test-Path $envPath) {
    # 读取现有内容
    $envContent = Get-Content $envPath -Raw
    
    # 更新ALLOWED_HOSTS
    if ($envContent -match "ALLOWED_HOSTS=") {
        # 如果已存在，追加新IP
        $envContent = $envContent -replace "ALLOWED_HOSTS=([^\r\n]*)", "ALLOWED_HOSTS=localhost,127.0.0.1,$selectedIP"
    } else {
        # 如果不存在，添加新行
        $envContent += "`nALLOWED_HOSTS=localhost,127.0.0.1,$selectedIP`n"
    }
    
    # 更新CORS_ALLOWED_ORIGINS
    if ($envContent -match "CORS_ALLOWED_ORIGINS=") {
        $envContent = $envContent -replace "CORS_ALLOWED_ORIGINS=([^\r\n]*)", "CORS_ALLOWED_ORIGINS=http://localhost:8501,http://127.0.0.1:8501,http://${selectedIP}:8501"
    } else {
        $envContent += "CORS_ALLOWED_ORIGINS=http://localhost:8501,http://127.0.0.1:8501,http://${selectedIP}:8501`n"
    }
    
    # 写回文件
    $envContent | Set-Content $envPath -NoNewline
    Write-Host "  ✅ Django配置已更新" -ForegroundColor Green
} else {
    Write-Host "  ❌ 未找到study\.env文件，请先创建该文件" -ForegroundColor Red
}

Write-Host ""

# 3. 更新前端配置
Write-Host "步骤3：更新Streamlit配置..." -ForegroundColor Yellow

$settingsPath = "前端\config\settings.py"

if (Test-Path $settingsPath) {
    $content = Get-Content $settingsPath -Raw
    
    # 替换API_BASE_URL
    $content = $content -replace 'API_BASE_URL = "http://localhost:8000/api/v1"', "API_BASE_URL = `"http://${selectedIP}:8000/api/v1`""
    $content = $content -replace "API_BASE_URL = f`"http://\{SERVER_IP\}:8000/api/v1`"", "API_BASE_URL = `"http://${selectedIP}:8000/api/v1`""
    
    $content | Set-Content $settingsPath -NoNewline
    Write-Host "  ✅ Streamlit配置已更新" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  未找到前端配置文件" -ForegroundColor Yellow
}

Write-Host ""

# 4. 检查Streamlit配置文件
Write-Host "步骤4：检查Streamlit服务器配置..." -ForegroundColor Yellow

$streamlitConfigPath = "前端\.streamlit\config.toml"
$streamlitConfigDir = "前端\.streamlit"

if (-not (Test-Path $streamlitConfigDir)) {
    New-Item -ItemType Directory -Path $streamlitConfigDir -Force | Out-Null
}

$streamlitConfig = @"
[server]
headless = true
address = "0.0.0.0"
port = 8501
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
"@

$streamlitConfig | Set-Content $streamlitConfigPath
Write-Host "  ✅ Streamlit服务器配置已更新" -ForegroundColor Green

Write-Host ""

# 5. 检查防火墙
Write-Host "步骤5：配置Windows防火墙..." -ForegroundColor Yellow

try {
    # 检查是否以管理员运行
    $isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    
    if ($isAdmin) {
        # 开放Django端口
        $rule8000 = Get-NetFirewallRule -DisplayName "Django Backend" -ErrorAction SilentlyContinue
        if (-not $rule8000) {
            New-NetFirewallRule -DisplayName "Django Backend" -Direction Inbound -Protocol TCP -LocalPort 8000 -Action Allow | Out-Null
            Write-Host "  ✅ 已开放Django端口(8000)" -ForegroundColor Green
        } else {
            Write-Host "  ℹ️  Django端口(8000)已开放" -ForegroundColor Cyan
        }
        
        # 开放Streamlit端口
        $rule8501 = Get-NetFirewallRule -DisplayName "Streamlit Frontend" -ErrorAction SilentlyContinue
        if (-not $rule8501) {
            New-NetFirewallRule -DisplayName "Streamlit Frontend" -Direction Inbound -Protocol TCP -LocalPort 8501 -Action Allow | Out-Null
            Write-Host "  ✅ 已开放Streamlit端口(8501)" -ForegroundColor Green
        } else {
            Write-Host "  ℹ️  Streamlit端口(8501)已开放" -ForegroundColor Cyan
        }
    } else {
        Write-Host "  ⚠️  需要管理员权限才能配置防火墙" -ForegroundColor Yellow
        Write-Host "  请以管理员身份运行此脚本，或手动开放端口8000和8501" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ⚠️  配置防火墙时出错：$($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  配置完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "📋 访问地址：" -ForegroundColor Yellow
Write-Host ""
Write-Host "  👨‍💼 管理员（仅服务器本机）：" -ForegroundColor Cyan
Write-Host "    Django Admin: http://localhost:8000/admin/" -ForegroundColor White
Write-Host ""
Write-Host "  👥 学生用户（内网PAD/手机/电脑）：" -ForegroundColor Cyan
Write-Host "    学习系统:     http://$selectedIP:8501" -ForegroundColor Green
Write-Host ""
Write-Host "  ⚠️  学生只需访问Streamlit前端，无需访问Django后台" -ForegroundColor Yellow
Write-Host ""

Write-Host "🔄 重启服务：" -ForegroundColor Yellow
Write-Host "  1. 重启Django后端：" -ForegroundColor Cyan
Write-Host "     cd study" -ForegroundColor White
Write-Host "     python manage.py runserver 0.0.0.0:8000" -ForegroundColor White
Write-Host ""
Write-Host "  2. 重启Streamlit前端：" -ForegroundColor Cyan
Write-Host "     cd 前端" -ForegroundColor White
Write-Host "     streamlit run app.py" -ForegroundColor White
Write-Host ""

Write-Host "👤 测试登录：" -ForegroundColor Yellow
Write-Host "  用户名：admin" -ForegroundColor White
Write-Host "  密码：  123456" -ForegroundColor White
Write-Host ""

Write-Host "按任意键退出..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

