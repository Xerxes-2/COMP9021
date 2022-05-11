Write-Host 'polys_3.txt:'
Compare-Object (python .\test_ori.py polys_3.txt) (python .\test_new.py polys_3.txt)