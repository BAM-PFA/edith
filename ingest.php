<?php

// ############################################
// -------- USER INPUT ------------------------
$targetdir = '/Users/RLAS_Admin/Sites/ingest/uploads/';
$user = $_POST["user"];
// ############################################


// ############################################
// ----PROCESS FILES SELECTED BY THE USER -----

$total = count($_FILES['file']['tmp_name']);
echo $total;

foreach($_FILES['file']['tmp_name'] as $key => $tmp_name ){
    $file_name = $_FILES['file']['name'][$key];
    // $file_size = $_FILES['file']['size'][$key];
    $file_tmp = $_FILES['file']['tmp_name'][$key];
    // $file_type = $_FILES['file']['type'][$key];
    $basename = basename($file_name);
    
	if ($metadataStatus == 'accept') {
		
		// include 'metadataFetch.php'; 
		// include 'evaluate.php';
		echo $basename;
		// $uploadedfile = $targetdir . $basename;
	}
}



// echo '<form method="post" action=''>
// 	<div>
// 	   <label for="accept">Accept</label>
// 	   <input type="submit" name="accept"/><br/>
// 	</div>
// 	</form>';
// ############################################

// ############################################
// ---- RUN PYTHON INGEST SCRIPT --------------
$command = escapeshellcmd("/usr/local/bin/python3 /Users/RLAS_Admin/Sites/ingest/ingest.py " . $user);

// ---- AND DISPLAY THE RESULTS -----
// THIS VERSION OUTPUTS THE BASH STUFF IN REAL TIME, BUT NOT THE PYTHON OUTPUT...
while (@ ob_end_flush()); // end all output buffers if any

$proc = popen($command, 'r');
echo '<pre>';
while (!feof($proc))
{
    echo fread($proc, 4096);
    @ flush();
}
echo '</pre>';
// BUT THIS VERSION SHOWS EVERYTHING AFTER ALL PROCESSING IS DONE
// $output = shell_exec($command . " 2>&1");
// echo $output;
// ############################################

echo "Goodbye!"

?>
