<?php

$command = escapeshellcmd("/usr/local/bin/python3 /Users/bampfa/Sites/ingest/basicQuery.py " . $basename);
exec($command, $output);
$stuff = strval($output[1]);
$data = json_decode($stuff);
// echo $output[1];

// print_r($data);
unset($output);


// Open the table
echo "<table>";


echo "<tr>";
echo "<td>filename</td>";
echo "<td>$basename</td>";
echo "</tr>";

echo "<tr>";
echo "<td>title</td>";
echo "<td>$data->title</td>";
echo "</tr>";


// Close the table
echo "</table>";





// if (count($data->title)) {
//         // Open the table
//         echo "<table>";

//         // Cycle through the array
//         foreach ($data->title as $index => $title) {

//             // Output a row
//             echo "<tr>";
//             // echo "<td>$basename</td>";
//             echo "<td>$title->title</td>";
//             echo "</tr>";
//         }

//         // Close the table
//         echo "</table>";
//     }


?>