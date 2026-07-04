# Sentinel-X HTTP Dev Server
# Run with: powershell -ExecutionPolicy Bypass -File dev-server.ps1

$port = 8000
$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://localhost:$port/")

try {
    $listener.Start()
    Write-Host "==========================================================" -ForegroundColor Cyan
    Write-Host "   SENTINEL-X LOCAL DEVELOPMENT SERVER" -ForegroundColor Green
    Write-Host "==========================================================" -ForegroundColor Cyan
    Write-Host " Server running at: http://localhost:$port/" -ForegroundColor Yellow
    Write-Host " Press [Ctrl+C] to stop the server" -ForegroundColor Gray
    Write-Host "==========================================================" -ForegroundColor Cyan
    Write-Host ""
}
catch {
    Write-Error "Failed to start listener. Is port $port already in use?"
    exit 1
}

$mimeTypes = @{
    ".html" = "text/html; charset=utf-8"
    ".css"  = "text/css; charset=utf-8"
    ".js"   = "application/javascript; charset=utf-8"
    ".json" = "application/json; charset=utf-8"
    ".png"  = "image/png"
    ".jpg"  = "image/jpeg"
    ".jpeg" = "image/jpeg"
    ".gif"  = "image/gif"
    ".svg"  = "image/svg+xml"
    ".ico"  = "image/x-icon"
    ".pdf"  = "application/pdf"
}

# Resolve project root (parent's parent of this scripts folder, or fallback to current dir)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if ($null -eq $scriptDir -or $scriptDir -eq "") {
    $scriptDir = Get-Location
}
$projectRoot = (Resolve-Path (Join-Path $scriptDir "..\..")).Path
if (!(Test-Path (Join-Path $projectRoot "README.md"))) {
    $projectRoot = (Get-Location).Path
}

while ($listener.IsListening) {
    try {
        $context = $listener.GetContext()
        $request = $context.Request
        $response = $context.Response

        $rawUrl = $request.RawUrl.Split('?')[0] # Strip query parameters
        
        # API Error Logging Endpoint
        if ($rawUrl -eq "/api/log-error") {
            $reader = New-Object System.IO.StreamReader($request.InputStream)
            $body = $reader.ReadToEnd()
            Write-Host "================== FRONTEND ERROR ==================" -ForegroundColor Red
            Write-Host $body -ForegroundColor Yellow
            Write-Host "====================================================" -ForegroundColor Red
            
            $response.StatusCode = 200
            $response.ContentType = "application/json"
            $resBytes = [System.Text.Encoding]::UTF8.GetBytes('{"status":"ok"}')
            $response.ContentLength64 = $resBytes.Length
            $response.OutputStream.Write($resBytes, 0, $resBytes.Length)
            $response.Close()
            continue
        }

        # Determine target file path
        if ($rawUrl -eq "/" -or $rawUrl -eq "") {
            $response.Redirect("/frontend/src/index.html")
            $response.Close()
            continue
        } else {
            # Sanitize path to prevent directory traversal
            $relative = $rawUrl.TrimStart('/') -replace '/', '\'
            $localPath = Join-Path $projectRoot $relative
        }

        # Resolve directory queries
        if (Test-Path $localPath -PathType Container) {
            $localPath = Join-Path $localPath "index.html"
        }

        if (Test-Path $localPath) {
            $ext = [System.IO.Path]::GetExtension($localPath).ToLower()
            $mime = $mimeTypes[$ext]
            if ($null -eq $mime) { $mime = "application/octet-stream" }

            $response.ContentType = $mime
            $response.StatusCode = 200

            # Read and write file bytes
            $bytes = [System.IO.File]::ReadAllBytes($localPath)
            $response.ContentLength64 = $bytes.Length
            $response.OutputStream.Write($bytes, 0, $bytes.Length)
            
            Write-Host "[200] $($request.HttpMethod) $($request.RawUrl) -> $mime" -ForegroundColor Green
        } else {
            $response.StatusCode = 404
            $response.ContentType = "text/plain"
            $errBytes = [System.Text.Encoding]::UTF8.GetBytes("404 Not Found: $rawUrl")
            $response.ContentLength64 = $errBytes.Length
            $response.OutputStream.Write($errBytes, 0, $errBytes.Length)

            Write-Host "[404] $($request.HttpMethod) $($request.RawUrl) - Not Found" -ForegroundColor Red
        }
    }
    catch {
        if ($listener.IsListening) {
            Write-Host "Error serving request: $_" -ForegroundColor Yellow
        }
    }
    finally {
        if ($null -ne $response) {
            $response.Close()
        }
    }
}
