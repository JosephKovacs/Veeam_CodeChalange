param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$SourceFolder,
    [Parameter(Mandatory=$true, Position=1)]
    [string]$ReplicaFolder,
    [Parameter(Mandatory=$true, Position=2)]
    [string]$LogFilePath
)

$Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# Ensure that the source and replica folders exist
if (!(Test-Path $SourceFolder)) {
    Write-Error "Source folder not found: $SourceFolder"
    $Message = "Source folder not found: $SourceFolder."
    # Append log message to file
    $Timestamp + " " + $Message | Out-File -FilePath $LogFilePath -Append

    exit 1
}
if (!(Test-Path $ReplicaFolder)) {
    New-Item -ItemType Directory -Path $ReplicaFolder | Out-Null
}

# Get all files and folders in the source folder
$items = Get-ChildItem -Path $SourceFolder -Recurse

$Message = "Get all files and folders in the source folder:"
$Timestamp + " " + $Message | Out-File -FilePath $LogFilePath -Append
Get-ChildItem -Path $SourceFolder -Recurse | Out-File -FilePath $LogFilePath -Append


# Copy each item to the replica folder
foreach ($item in $items) {
    $destination = $item.FullName.Replace($SourceFolder, [string]$ReplicaFolder)
    if ($item.PSIsContainer) {
        if (!(Test-Path $destination)) {
            New-Item -ItemType Directory -Path $destination | Out-Null
        }
    } else {
        Copy-Item -Path $item.FullName -Destination $destination -Force | Out-File -FilePath $LogFilePath -Append
    }
}

# Remove any items in the replica folder that don't exist in the source folder
$replicaItems = Get-ChildItem -Path $replica -Recurse

$Message = "Remove any items in the replica folder that don't exist in the source folder:"
$Timestamp + " " + $Message | Out-File -FilePath $LogFilePath -Append
Get-ChildItem -Path $replica -Recurse | Out-File -FilePath $LogFilePath -Append


foreach ($replicaItem in $replicaItems) {
    $sourceItem = $replicaItem.FullName.Replace($replica, $source)
    if (!(Test-Path $sourceItem)) {
        if ($replicaItem.PSIsContainer) {
            Remove-Item -Path $replicaItem.FullName -Recurse -Force | Out-File -FilePath $LogFilePath -Append
        } else {
            Remove-Item -Path $replicaItem.FullName -Force | Out-File -FilePath $LogFilePath -Append
        }
    }
}


$Message = "Synchronization complete."
# Append log message to file
$Timestamp + " " + $Message | Out-File -FilePath $LogFilePath -Append
