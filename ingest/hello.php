<?php

$targetdir = '/Users/RLAS_Admin/Sites/ingest/uploads/';   
      // name of the directory where the files should be stored
// $targetfile = $targetdir.$_FILES['file']['name'];
$uploadedfile = $targetdir . basename($_FILES['file']['name']);

if (move_uploaded_file($_FILES['file']['tmp_name'], $uploadedfile)) {
    // file uploaded succeeded
} else { 
    // file upload failed
	echo "failure";

}
print_r($_FILES);
// $file = $_FILES["file"]["name"];
$user = $_POST["user"];

echo $user;

$command = escapeshellcmd('/usr/local/bin/python3 /Users/RLAS_Admin/Sites/ingest/hello.py' . $uploadedfile . $user);
// $command = escapeshellcmd('/usr/local/bin/python3 /Users/RLAS_Admin/Sites/ingest/help.py' . );
$output = shell_exec($command);
echo $output;

?>
