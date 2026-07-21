param([string]$Key = "CHANGE_ME", [string]$VpsHost = "tv-signal.srv1695304.hstgr.cloud")
$body = @{ event = "TEST_SWEEP"; symbol = "US100"; tf = "15"; price = 29000.5
           t = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds() } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "https://$VpsHost/tv-signal?key=$Key" -ContentType "application/json" -Body $body
Write-Host "If ok:true came back, check tv_signals.jsonl on GitHub - the loop is closed."
