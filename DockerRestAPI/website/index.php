<html>
    <head>
        <title>CIS 322 REST-api demo: Laptop list</title>
    </head>
    <!-- Our own style sheet -->
   <link rel="stylesheet" href="/static/css/calc.css" /> 

    <body>
        <h1>Open Times</h1>
        <ul>
            <?php
            $json = file_get_contents('http://time_calc-service/listAll');
            $obj = json_decode($json);
	          $laptops = $obj->opentimes;
            foreach ($laptops as $l) {
                echo "<li>$l</li>";
            }
            ?>
        </ul>
        <h1>close Times</h1>
        <ul>
            <?php
            $json = file_get_contents('http://time_calc-service/listAll');
            $obj = json_decode($json);
	          $laptops = $obj->closetimes;
            foreach ($laptops as $l) {
                echo "<li>$l</li>";
            }
            ?>
        </ul>
    </body>
</html>

