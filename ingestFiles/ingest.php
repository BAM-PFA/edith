<?php

// ############################################
// -------- USER INPUT ------------------------
$targetdir = '/Users/RLAS_Admin/Sites/ingest/uploads/';
$user = $_POST["user"];
// ############################################


// ############################################
// ----PROCESS FILES SELECTED BY THE USER -----

$total = count($_FILES['file']['tmp_name']);
// echo $total;

echo '<script src="jquery-1.7.1.js" type="text/javascript"></script>
<script src="jquery.confirm.js" type="text/javascript"></script>
<script type="text/javascript">
    $(function(){
        function confirmclose() {
                return "Are you sure? you want to close";
        }
        window.onbeforeunload = confirmclose;
    });
</script>';

foreach($_FILES['file']['tmp_name'] as $key => $tmp_name ){
    $file_name = $_FILES['file']['name'][$key];
    $file_name = preg_replace('/\s+/', '_', $file_name);
    // $file_size = $_FILES['file']['size'][$key];
    $file_tmp = $_FILES['file']['tmp_name'][$key];
    // $file_type = $_FILES['file']['type'][$key];
    $basename = basename($file_name);
    // echo $basename . "HEY THERE";
	
    $uploadedfile = $targetdir . basename($file_name);
    include 'metadatafetch.php';
    if (move_uploaded_file($file_tmp, $uploadedfile)) {
	    // file uploaded succeeded
		// echo "success";


	} else { 
    // file upload failed
		echo "FILE UPLOAD FOR ".$basename." FAILED";

	}
}

// ############################################

// ############################################
// ---- RUN PYTHON INGEST SCRIPT --------------
$command = escapeshellcmd("/usr/local/bin/python3 /Users/RLAS_Admin/Sites/ingest/ingestFiles/ingest.py " . $user . " 2>&1");

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

echo "<br><br>Goodbye!"

?>
