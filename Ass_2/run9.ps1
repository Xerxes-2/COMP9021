Write-Host 'polys_9_wrong_2.txt:'
Compare-Object (python .\test_ori.py polys_9_wrong_2.txt) (python .\test_new.py polys_9_wrong_2.txt)