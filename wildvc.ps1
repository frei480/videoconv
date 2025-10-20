$currentPath = $MyInvocation.MyCommand.Path | split-path -parent
$inputFolder = $currentPath + '/input/'
$outputFolder = $currentPath + '/output/'
$ffmpeg = $currentPath + '/ffmpeg/ffmpeg.exe'

foreach($file in Get-ChildItem -Path $inputFolder)
{
	Write-Host "------------Started next------------"
	
	$arg = '-i "' + $file.FullName + '" -c:v libx265 -c:a copy "' + $outputFolder + $file.Name +'"'
	
	Invoke-Expression "& $ffmpeg $arg"
}

Read-Host -Prompt "Press any key to exit...:"