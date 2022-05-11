Write-Host 'polys_1.txt:'
Compare-Object (python .\test_ori.py polys_1.txt) (python .\test_new.py polys_1.txt)