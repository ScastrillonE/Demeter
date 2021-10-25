var tblCompras_Data_Table;
let valores = [];
let material_id = [];

var compras = {
    items: {
        cliente: '',
        total: 0,
        material: []
    },
    add: function (cliente,tot,item) {
        let client = document.getElementById('id_client_name');
        let tota = compras.calculate_total();
        this.items.cliente = client.value;
        this.items.total = tota;
        this.items.material.push(item);
    },

    calculate_total: function(){
        let total = 0;
        var table = document.getElementById("tablaprueba");
        let tr_list = table.tHead.getElementsByTagName('tr');
        for(let i = 1;i<tr_list.length;i++){
            let td_list = tr_list.item(i).getElementsByTagName('td')
            var total_unitario = td_list.item(3).getElementsByTagName('input').item(0).value;
            total += parseFloat(total_unitario);
        }
        document.getElementById('id_total').value = total;
        return total
    },

    agregar_fila: function(){
        var table = document.getElementById("tablaprueba");
        table.insertRow(-1).innerHTML = '<td><select class="material_select" style="width: 90px;"></select></td><td><input type="text" size=10 onkeyup="calcular_total_unitario(this)"></input></td><td><input type="text" size=10 onkeyup="calcular_total_unitario(this)"></input></td><td><input disabled type="text" size=6 value=0></input></td><td><button type="button" class="btn btn-primary" onclick="compras.agregar_fila()">G</button></td>';
        
        this.agregar();
        this.calculate_total();
    },

    obtener_valores: function () {
        let material_list = document.getElementsByClassName('material_select')
        let materialCount = material_list.length;
        var table = document.getElementById("tablaprueba");
		let RowCount = table.rows.length;

        for (var c = 0; c < materialCount; c++){
            material_id.push(material_list.item(c).value);
        }
        for (var i = 1;i < RowCount;i++){
            var row = table["rows"][i];
            var td_list = row.getElementsByTagName('td');
            var td_count = td_list.length -1;
            for(var j = 1; j < td_count;j++){
                var td = td_list[j].getElementsByTagName('input')
                if(td){
                    valores.push(td.item(0).value);
                }
            }
        }
        
	},
    crear_items: () => {
        let it;
        let primero = 0;
        let ultimo = 3;
        for(var i = 0;i < material_id.length;i++){
            let division = valores.length / 4;
            let lista = valores.slice(primero,ultimo);
            for(var j = 0;j < division;j++){
                it = {'id':material_id[i],'kilos':lista[0],'valor_uni':lista[1],'total':lista[2]}
            }
            primero += 3;
            ultimo += 3;
            compras.add('',0,it);
        }
    },
    insertar_valores_update: (list_material) => {
        var table = document.getElementById("tablaprueba");
        table.deleteRow(1);
        list_material.forEach(element => {
            table.insertRow(-1).innerHTML = `<td><select class="material_select" style="width: 90px;">  <option value="${element['id']}" selected>${element['name']}</option></select></td><td><input type="text" size=10 onkeyup="calcular_total_unitario(this)" value=${element['kilos']}></input></td><td><input type="text" size=10 onkeyup="calcular_total_unitario(this)" value=${element['valor_uni']}></input></td><td><input disabled type="text" size=6 value=${element['total']}></input></td><td><button type="button" class="btn btn-primary" onclick="compras.agregar_fila()">G</button></td>`;
            compras.agregar();
        });
        compras.calculate_total();
        
    },
    agregar: () => {
        $('.material_select').select2({
            theme: "bootstrap4",
            language: 'es',
            allowClear: true,
            ajax: {
                delay: 250,
                type: 'POST',
                url: window.location.pathname,
                data: function (params) {
                    var queryParameters = {
                        term: params.term,
                        action: 'search_materiales',
                        'csrfmiddlewaretoken': '{{ csrf_token }}',
                    }
                    return queryParameters;
                },
                processResults: function (data) {
                    return {
                        results: $.map(data, function(obj) {
                        return { id: obj.id, text: obj.name };
                        })
                    };
                },
            },
            placeholder: 'Ingrese el material',
            minimumInputLength: 1,
        });
    }
    /* agregar: () => {
        var csrftoken = Cookies.get('csrftoken');
        $.ajax(
            {
              url : window.location.pathname,
              type: "POST",
              data : {action: 'search_materiales','csrfmiddlewaretoken':csrftoken}
            })
              .done(function(data) {
                let s = document.getElementsByClassName('material_select');
                for(var i = 0; i < s.length;i++){
                    if(s.item(i).options.length == 0){
                        for(var j = 0;j <= data.length;i++){
                            let s = document.getElementsByClassName('material_select');

                            const option = document.createElement('option');
                            option.value = data[i]['id'];
                            option.text = data[i]['name'];
                            s.item(i).appendChild(option);
                            }
                    }
                    
                }
              })
              .fail(function(data) {
                alert( "error" );
              });
        
      } */
}


/* $("#tblcompras tbody").on('click', "a[rel='remove']",()=>{
    var tr = tblCompras.cell($(this).closest('tr, t')).index();
    console.log(tr.row);
}); */
$('#tblcompras tbody').on('click', "a[rel='remove']", function () {
    /* var data = tblCompras_Data_Table.row( this );
    console.log(data.row().indexes())
    compras.items.material.splice(data.row, 1); */
    var tr = $(this).closest("tr").index()
    compras.items.material.splice(tr, 1);

    compras.list();
    compras.calculate_total();
    /* if(compras.items.material.length === 0){
        compras.items.material.splice(data['id'], 1);
    }else{
        compras.items.material.splice(data['id']-1, 1);
    }
    compras.list()
    compras.calculate_total(); */
});

document.getElementById('id_btn_guardar').addEventListener('click',function guardar(e){
    e.preventDefault();
    compras.obtener_valores()
    compras.crear_items()
    var csrftoken = Cookies.get('csrftoken');
    compras.items.cliente = $('#id_client_name').val();
    compras.items.total = document.getElementById("id_total").value;
    var datos = compras.items
    console.log(datos)

    const data = new FormData();
    data.append('action',$("#id_action").val())
    data.append('datos',JSON.stringify(datos))
    data.append('representation',JSON.stringify(datos))

    fetch(window.location.pathname,{
        method:'POST',
        body:data
    })
    .then(function(response){
        if(response.ok){
            return response.json()
        }
        else{
            console.log("Error en la llamada ajax")
        }
    })
    .then((data)=>{
        console.log(data)
        if(!data["error"]){
            $.notify(data["success"],'success');
            let id = data['id_guardado']
            location.href="/compras/pdf/print/" + id + "/"
        }
        $.notify(data["error"],'danger');

    })
    .catch(function(err) {
        console.log(err);
     });

}
);

function calcular_total_unitario(celda){
    let celda_calcular =  celda.parentNode.parentNode;
    let td_list = celda_calcular.getElementsByTagName('td');
    let kilos = td_list.item(1).getElementsByTagName('input').item(0);
    let val_uni = td_list.item(2).getElementsByTagName('input').item(0);
    let total = td_list.item(3).getElementsByTagName('input').item(0);
    let calculo = Number(kilos.value) * Number(val_uni.value);
    total.value = Math.round(calculo,1);
    compras.calculate_total()
}
