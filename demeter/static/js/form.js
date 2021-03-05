var tblCompras_Data_Table;
var compras = {
    items: {
        cliente: '',
        total: 0,
        material: []
    },
    add: function (cliente,tot,item) {
        this.items.cliente = cliente;
        this.items.total = tot;
        this.items.material.push(item);
        this.list();
        this.calculate_total();
    },

    calculate_total: function(){
        let total = 0;
        compras["items"].material.forEach(element => {
            total += element.total;
        });
        document.getElementById("id_total").value = total;
    },

    list: function () {
        
        tblCompras_Data_Table = $('#tblcompras').DataTable({
            
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.items.material   ,
            columns: [
                {"data": "name"},
                {"data": "kilos"},
                {"data": "valor_uni"},
                {"data": "bonus"},
                {"data": "total"},
            ],
            columnDefs: [
                {
                    targets: [5],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        botones = '<a rel="remove" class="btn btn-danger btn-xs btn-flat" style="color: white;"><i class="fas fa-trash-alt"></i></a>';
                        return botones;
                    }
                },
                {
                    targets: [0],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<span class="badge badge-secondary">' + data + '</span>';
                    }
                },
                
                {
                    targets: [1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        //'<input type="text" name="cant" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.valor_uni + '">'
                        return "$" + data;
                    }
                },
                {
                    targets: [3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return data;
                    }
                },
                {
                    targets: [4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return  '$' + parseFloat(data).toFixed(2);
                    }
                },
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {

            },
            initComplete: function (settings, json) {

            }
        });
       
    },
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
        alert(data["success"]);
    })
    .catch(function(err) {
        console.log(err);
     });

}
);
