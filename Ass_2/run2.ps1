Write-Host 'polys_2.txt:'
Compare-Object (python .\test_ori.py polys_2.txt) (python .\test_new.py polys_2.txt)