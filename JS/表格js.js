//新增数据函数
function addshuju(){
        var table = document.getElementById("table");
        //console.log(table);
        //获取插入位置
        var length = table.rows.length;
        //console.log(length);
        //插入行节点
        var newshuju = table.insertRow(length);
        console.log(newshuju);       
       //newshuju.innerHTML = '114514';
       //插入列节点对象
       var namecol = newshuju.insertCell(0);
       var classcol = newshuju.insertCell(1);
       var spendcol = newshuju.insertCell(2);
       var waycol = newshuju.insertCell(3);
       var actioncol = newshuju.insertCell(4);
       console.log(newshuju);
       //修改节点文本内容
       namecol.innerHTML = '输入你的大名';
       classcol.innerHTML = '输入你的班级';
        spendcol.innerHTML = '你要多少钱';
       waycol.innerHTML = '拿去做甚么';
       actioncol.innerHTML = '<button onclick="editshuju(this)">编辑</button><button onclick= "deleteshuju(this)">删除</button>';
        }
       //删除数据函数
        function deleteshuju(button){
                //console.log(button);
         var row = button.parentNode.parentNode;
         //console.log(row) 
         row.parentNode.removeChild(row);      
        }
    //编辑数据函数
        function editshuju(button){
                //console.log(button);
        var row = button.parentNode.parentNode;
        var name = row.cells[0];
        var classes = row.cells[1];
        var spend = row.cells[2];
        var way = row.cells[3];
        var action = row.cells[4];

        var inputname = prompt ("输入你的大名");
        var inputclass = prompt ("哪个班");
        var inputspend = prompt ("how much");
        var inputwhat = prompt ("what to do");
        name.innerHTML = inputname;
        classes.innerHTML = inputclass;
        spend.innerHTML = inputspend;
        way.innerHTML = inputwhat;
        if(inputname ==0 ){
                alert( '速速报上名来');
        }                                                                          
        }
        
    