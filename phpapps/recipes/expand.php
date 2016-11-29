<html>
<style>
.FAQ { 
    vertical-align: top; 
    height:auto !important; 
}
.list {
    display:none; 
    height:auto;
    margin:0;
    float: left;
}
.show {
    display: none; 
}
.hide:target + .show {
    display: inline; 
}
.hide:target {
    display: none; 
}
.hide:target ~ .list {
    display:inline; 
}

/*style the (+) and (-) */
.hide, .show {
	width: 30px;
	height: 30px;
	!border-radius: 30px;
	font-size: 20px;
	color: #000;
	text-shadow: 0 1px 0 #666;
	text-align: center;
	text-decoration: none;
	!box-shadow: 1px 1px 2px #000;
	!background: #cccbbb;
	opacity: .95;
	margin-right: 0;
	float: left;
	margin-bottom: 25px;
}

.hide:hover, .show:hover {
	color: #eee;
	text-shadow: 0 0 1px #666;
	text-decoration: none;
	!box-shadow: 0 0 4px #222 inset;
	opacity: 1;
	margin-bottom: 25px;
}

.list p{
    height:auto;
    margin:0;
}
.question {
	float: left;
	height: auto;
	width: 90%;
	line-height: 20px;
	padding-left: 20px;
	margin-bottom: 25px;
	font-style: italic;
}
</style>
</html>

<div class="FAQ">
    <a href="#hide1" class="hide" id="hide1">+</a>
    <a href="#show1" class="show" id="show1">-</a>
    <div class="question"> Question Question Question Question Question Question Question Question Question Question Question? </div>
        <div class="list">
            <select>
            <option>fdfsdd</option>
            </select>
            <p>Answer Answer Answer Answer Answer Answer Answer Answer Answer Answer Answer Answer Answer Answer Answer Answer Answer Answer </p>
        </div>
</div>