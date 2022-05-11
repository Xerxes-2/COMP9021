Write-Host 'polys_10_wrong_3.txt:'
Compare-Object (python .\test_ori.py polys_10_wrong_3.txt) (python .\test_new.py polys_10_wrong_3.txt)