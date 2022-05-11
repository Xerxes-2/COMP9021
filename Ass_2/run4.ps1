Write-Host 'polys_4.txt:'
Compare-Object (python .\test_ori.py polys_4.txt) (python .\test_new.py polys_4.txt)