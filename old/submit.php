<?php


	if (move_uploaded_file($file_tmp, $uploadedfile)) {
	    // file uploaded succeeded
		echo "success";

	} else { 
    // file upload failed
		echo "failure";

	}

?>