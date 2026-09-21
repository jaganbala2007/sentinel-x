# Fast Sentinel-X Automated Release Packager for Raspberry Pi OS
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem

$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$zipPath = Join-Path $root "Sentinel-X-Complete.zip"

Write-Host "[Sentinel-X Packager] Building high-speed deployment ZIP package..."

if (Test-Path $zipPath) {
    Remove-Item -Force $zipPath
}

$excludeDirs = @(
    ".git", ".github", "__pycache__", ".pytest_cache", ".venv", "venv",
    "node_modules", ".idea", ".vscode", "scratch", ".agents", "college id",
    "90-Degree Turn Detection.v1i.folder", "room.v1i.folder", ".system_generated"
)

$excludeFiles = @(
    ".DS_Store", "Sentinel-X-Complete.zip", "sentinel_edge.db-journal",
    "Zipped PDF Files.zip", "sentinel-x-frontend.zip", "app.html.scada.bak"
)

$textExtensions = @(
    ".sh", ".py", ".json", ".yaml", ".yml", ".txt", ".md", ".html",
    ".js", ".css", ".conf", ".service", ".env", ".example", ".sql",
    ".ini", ".desktop"
)

$zipStream = [System.IO.File]::Open($zipPath, [System.IO.FileMode]::Create)
$archive = New-Object System.IO.Compression.ZipArchive($zipStream, [System.IO.Compression.ZipArchiveMode]::Create)

$count = 0

function Collect-And-Zip($currentDir) {
    $items = Get-ChildItem -LiteralPath $currentDir
    foreach ($item in $items) {
        if ($item.PSIsContainer) {
            if ($excludeDirs -contains $item.Name) { continue }
            Collect-And-Zip $item.FullName
        } else {
            if ($excludeFiles -contains $item.Name) { continue }
            if ($item.Extension -in @(".zip", ".pyc", ".pyo", ".pyd", ".tmp", ".log")) { continue }

            $relPath = $item.FullName.Substring($root.Length + 1)
            $unixRel = $relPath.Replace("\", "/")
            $entryName = "Sentinel-X-Complete/$unixRel"

            $entry = $archive.CreateEntry($entryName, [System.IO.Compression.CompressionLevel]::Fastest)
            $entryStream = $entry.Open()

            if ($textExtensions -contains $item.Extension.ToLower() -or $item.Name -in @("VERSION", "LICENSE", "CODEOWNERS", ".gitignore", ".env.example")) {
                $content = [System.IO.File]::ReadAllText($item.FullName)
                # Normalize CRLF -> Unix LF
                $contentLf = $content -replace "`r`n", "`n" -replace "`r", "`n"
                $bytes = [System.Text.Encoding]::UTF8.GetBytes($contentLf)
                $entryStream.Write($bytes, 0, $bytes.Length)
            } else {
                $fileStream = [System.IO.File]::OpenRead($item.FullName)
                $fileStream.CopyTo($entryStream)
                $fileStream.Dispose()
            }

            $entryStream.Dispose()
            $global:count++
        }
    }
}

Collect-And-Zip $root

$archive.Dispose()
$zipStream.Dispose()

$sizeMb = (Get-Item $zipPath).Length / 1MB
$hash = (Get-FileHash $zipPath -Algorithm SHA256).Hash

Write-Host "======================================================================"
Write-Host "   SENTINEL-X PORTABLE PACKAGE (PI OPTIMIZED) BUILT SUCCESSFULLY      "
Write-Host "======================================================================"
Write-Host "  Package Path: $zipPath"
Write-Host "  File Size:    $("{0:N2}" -f $sizeMb) MB"
Write-Host "  Total Files:  $count"
Write-Host "  SHA256 Hash:  $hash"
Write-Host "======================================================================"
