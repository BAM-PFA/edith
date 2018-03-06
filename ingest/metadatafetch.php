<?php

$command = escapeshellcmd("/usr/local/bin/python3 /Users/RLAS_Admin/Sites/ingest/ingestFiles/basicQuery.py " . $basename);
// $output = array();
exec($command, $output);
$title = $output[1];
$altTitle = $output[2];
$accPref= $output[3];
$accDepos = $output[4];
$accItem = $output[5];
$projGroup = $output[6];
$country = $output[7];
$year = $output[8];
$directors = $output[9];
$credits = $output[10];
$notes = $output[11];
$condition = $output[12];





unset($output);


// Open the table
echo "<style>table, th, td {border: 1px solid black;}</style><table>";


echo "<tr>";
echo "<td>Filename</td>";
echo "<td>$basename</td>";
echo "</tr>";

echo "<tr>";
echo "<td>Title</td>";
echo "<td>$title</td>";
echo "</tr>";

echo "<tr>";
echo "<td>Alternative Title</td>";
echo "<td>$altTitle</td>";
echo "</tr>";

echo "<tr>";
echo "<td>Accession Number</td>";
echo "<td>$accPref-$accDepos-$accItem</td>";
echo "</tr>";

echo "<tr>";
echo "<td>Project/Group Title</td>";
echo "<td>$projGroup</td>";
echo "</tr>";

echo "<tr>";
echo "<td>Country of Production</td>";
echo "<td>$country</td>";
echo "</tr>";

echo "<tr>";
echo "<td>Release Year</td>";
echo "<td>$year</td>";
echo "</tr>";

echo "<tr>";
echo "<td>Director(s)</td>";
echo "<td>$directors</td>";
echo "</tr>";

echo "<tr>";
echo "<td>Credits</td>";
echo "<td>$credits</td>";
echo "</tr>";

echo "<tr>";
echo "<td>General Notes</td>";
echo "<td>$notes</td>";
echo "</tr>";

echo "<tr>";
echo "<td>Condition Notes from Original</td>";
echo "<td>$condition</td>";
echo "</tr>";

// Close the table
echo "</table>";



// if (count($data->title)) {
//		 // Open the table
//		 echo "<table>";

//		 // Cycle through the array
//		 foreach ($data->title as $index => $title) {

//			 // Output a row
//			 echo "<tr>";
//			 // echo "<td>$basename</td>";
//			 echo "<td>$title->title</td>";
//			 echo "</tr>";
//		 }

//		 // Close the table
//		 echo "</table>";
//	 }


?>