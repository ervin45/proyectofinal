<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
<title>Bieler Web Application</title>

<script type="text/javascript" src="/static/javascript/jquery/jquery.js"></script>
<script type="text/javascript" src="/static/jquery/javascript/interface.js"></script>

<link rel="stylesheet" type="text/css" href="/static/css/default.css" media="screen"/>

</head>
<body>



<div class="outer-container">

<div class="inner-container">
	<div class="header">
		<div class="title">
			<span class="sitename"><a href="index.html">${title}</a></span>
			<div class="slogan"></div>
		</div>		
	</div>
	<div class="path">	
			<a href="index.html">Home</a> &#8250; <a href="index.html">Subpage</a>
	</div>
${pt}
<table border="1">
    <tr>
        <td py:for="c in filas[0]"><a href="http://www.google.com.ar">${c}</a></td>
    </tr>
    <tr py:for="f in filas[1:]">
        <td><a href="/reportes/${link}">${f[0]}</a></td>
        <td py:for="c in f[1:]">${c}</td>
    </tr>
</table>
</div>
</div>
</body>
</html>
