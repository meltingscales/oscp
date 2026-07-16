Set-Location $PSScriptRoot

$folders = Get-ChildItem -Path . -Directory | Sort-Object Name

function Report {
    param(
        [string]$Label,
        [ConsoleColor]$Color,
        [scriptblock]$Filter
    )
    $total = 0
    foreach ($folder in $folders) {
        $items = Get-ChildItem -Path $folder.FullName -Directory | Where-Object $Filter | Sort-Object Name
        $count = $items.Count
        $total += $count
        Write-Host "  [$($folder.Name)] $count $Label" -ForegroundColor $Color
        foreach ($item in $items) {
            Write-Host "    -> $($item.Name)"
        }
    }
    Write-Host "[=] $total total $Label" -ForegroundColor $Color
    Write-Host ""
}

Report -Label "pwned" -Color Green -Filter { $_.Name -like '*.pwned' }
Report -Label "stuck" -Color Red -Filter { $_.Name -like '*.stuck' }
Report -Label "not complete" -Color Yellow -Filter { $_.Name -notmatch '\.' -and $_.Name -notlike '.*' }
