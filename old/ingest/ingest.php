<?php

$targetdir = '/Users/RLAS_Admin/Sites/ingest/uploads/';   
      // name of the directory where the files should be stored
// $targetfile = $targetdir.$_FILES['file']['name'];

$user = $_POST["user"];

foreach($_FILES['file']['tmp_name'] as $key => $tmp_name ){
    $file_name = $_FILES['file']['name'][$key];
    $file_size = $_FILES['file']['size'][$key];
    $file_tmp = $_FILES['file']['tmp_name'][$key];
    $file_type = $_FILES['file']['type'][$key];

	$uploadedfile = $targetdir . basename($file_name);
	echo $file_tmp . "<br/>" . $uploadedfile . "<br/>";

	if (move_uploaded_file($file_tmp, $uploadedfile)) {
	    // file uploaded succeeded
		echo "success";
		// $command = escapeshellcmd("/usr/local/bin/mediainfo " . $uploadedfile);

		// $command = escapeshellcmd("/usr/local/bin/python3 /Users/RLAS_Admin/Sites/ingest/hello.py" .
							  // " " . $uploadedfile . " " . $user);
		// $output = shell_exec($command . " 2>&1");
		// echo $output;
	} else { 
    // file upload failed
		echo "failure";

	}
// print_r($file);

$command = escapeshellcmd("/usr/local/bin/python3 /Users/RLAS_Admin/Sites/ingest/ingest.py" . " " . $user);
$output = shell_exec($command . " 2>&1");
echo $output;
echo $user;


echo "HELLO <br/>";

}



?>
