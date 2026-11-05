param(
  [Parameter(Mandatory=$true)][string]$InputJson,
  [Parameter(Mandatory=$true)][string]$OutputDir
)

$items = Get-Content -LiteralPath $InputJson -Raw -Encoding UTF8 | ConvertFrom-Json
[System.IO.Directory]::CreateDirectory($OutputDir) | Out-Null
$voice = New-Object -ComObject SAPI.SpVoice
$zhVoice = $voice.GetVoices() | Where-Object { $_.GetDescription() -like '*Huihui*' } | Select-Object -First 1
if ($null -ne $zhVoice) { $voice.Voice = $zhVoice }
$voice.Rate = 1
$voice.Volume = 100

foreach ($item in $items) {
  $stream = New-Object -ComObject SAPI.SpFileStream
  $path = Join-Path $OutputDir ("audio-{0:D2}.wav" -f [int]$item.index)
  $stream.Open($path, 3, $false)
  $previous = $voice.AudioOutputStream
  $voice.AudioOutputStream = $stream
  [void]$voice.Speak([string]$item.text)
  $voice.AudioOutputStream = $previous
  $stream.Close()
}

Write-Output ("created {0} narration files" -f $items.Count)
