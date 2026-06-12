# Total target boxes
$TOTAL = 30

# 1. Pwned Boxes
$pwnedDirs = Get-ChildItem -Path . -Directory | Where-Object { $_.Name -like '*.pwned' } | Sort-Object Name
$pwnedCount = $pwnedDirs.Count
$percent = [math]::Floor($pwnedCount * 100 / $TOTAL)
Write-Host "[+] $pwnedCount/$TOTAL boxes pwned ($percent%)" -ForegroundColor Green

# 2. Stuck Boxes
$stuckDirs = Get-ChildItem -Path . -Directory | Where-Object { $_.Name -like '*.stuck' } | Sort-Object Name
$stuckCount = $stuckDirs.Count
Write-Host "[-] $stuckCount boxes stuck on" -ForegroundColor Red
if ($stuckCount -gt 0) {
    $stuckDirs | ForEach-Object { Write-Host "  -> $($_.Name)" }
}

# 3. Non-Completed Boxes (Directories with no extensions)
$nonCompletedDirs = Get-ChildItem -Path . -Directory | Where-Object { $_.Name -notmatch '\.' -and $_.Name -notlike '.*' } | Sort-Object Name
$nonCompletedCount = $nonCompletedDirs.Count
Write-Host "[?] $nonCompletedCount boxes not complete" -ForegroundColor Yellow
if ($nonCompletedCount -gt 0) {
    $nonCompletedDirs | ForEach-Object { Write-Host "  -> $($_.Name)" }
}
