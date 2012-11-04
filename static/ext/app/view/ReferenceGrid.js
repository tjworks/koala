/**  var literatureStore = Ext.create('Ext.data.ArrayStore', {
        fields: [         
           {name:'_id'},
           {name: 'name'},
           {name: 'authors'},
           {name:'abstract'},
           {name:'entities'},
           {name:'processed_abstract'}
        ],
        data: []
    });
    */
 Ext.define('Precon.view.ReferenceGrid' ,{
    extend: 'Ext.grid.Panel',
    requires: [
        //'Ext.selection.CheckboxModel',
        'Ext.ux.RowExpander',
        'Precon.model.Reference'
    ],
    //selModel: Ext.create('Ext.selection.CheckboxModel'),
    id:'refgrid',
    alias : 'widget.referencegrid',

    title : 'References',
    multiSelect:true,
	
	//define the data
	store: Ext.create('Ext.data.ArrayStore', {
	  model:'Precon.model.Reference',
	  data:[]
	}),
	
	constructor: function(config) {
			//this.initConfig(config);
			return this.callParent(arguments);
	}, 
		
    initComponent: function() {
              this.columns = [
								{
								    text     : 'Title', 
								    width    : 75, 
								    flex:1,
								    sortable : true, 
								    dataIndex: 'name',
								    renderer: function(val, meta, record){
								    	return val
								    	//return '<a href="http://www.ncbi.nlm.nih.gov/pubmed?term='+ record.get('_id').substring(4)+'" target="pubmed">' + val+"</a>"
								    }
								   // renderer: change
								},
								{
								    text     : 'Author',
								   // flex     : 1,
								    sortable : false, 
								    width: 85,
								    dataIndex: 'authors'
								}
                          ];
     
              this.callParent(arguments);
    },
    height: 'auto',
    width: 'auto',
   // renderTo: Ext.getBody(),
    viewConfig: {
        stripeRows: true
    },
   
    plugins: [ {
    	ptype:'rowexpander',
    	rowBodyTpl:[
    	 '<b>Authors</b>: {authors}<br>',
    	 '<b>Abstract:</b><br>{processed_abstract}'
    	]	
    }],
    highlight:function(pubids, on){
    	for(var i=0;i<this.getStore().count();i++)
    		this.getView().removeRowCls(i, 'state-highlight')
    	for(var i=0;i<pubids.length;i++){        		
    		pubid = pubids[i]
    		if(pubid.indexOf("publ")<0) pubid = 'publ'+ pubid
    		var index = this.getStore().find('_id', pubid)
    		if(index>=0 && on) this.getView().addRowCls(index, 'state-highlight')    		
    	}
    },
    dockedItems: [{
        xtype: 'toolbar',
        dock: 'bottom',
        ui: 'footer',
        //margin:'0 0 20 0',
//      defaults: {minWidth: minButtonWidth},
        items: [
             { type: 'button', text: 'Export All References', handler:function(){ app.getController("Reference").exportReference() } },
             { type: 'button', text: 'Export Selected References', handler:function(){ app.getController("Reference").exportReference('selected') } }
        ]
    }]
   
});

/**
// create the data store
   
Ext.define('Precon.view.ReferenceGrid' ,{
    extend: 'Ext.grid.Panel',
    alias : 'widget.referencegrid',
    store: literatureStore,
    title:'References'});

    
    // create the Grid, see Ext.
    //literatureGrid=Ext.create('Ext.ux.LiveSearchGridPanel', {
        store: literatureStore,
        columnLines: true,
        columns: [                      
            {
                text     : 'Title', 
                width    : 75, 
                flex:1,
                sortable : true, 
                dataIndex: 'name',
                renderer: function(val, meta, record){
                	return '<a href="http://www.ncbi.nlm.nih.gov/pubmed?term='+ record.get('_id').substring(4)+'" target="pubmed">' + val+"</a>"
                }
               // renderer: change
            },
            {
                text     : 'Author',
               // flex     : 1,
                sortable : false, 
                width: 85,
                dataIndex: 'authors'
            }
        ],
        height: 'auto',
        width: 'auto',
       // renderTo: Ext.getBody(),
        viewConfig: {
            stripeRows: true
        },
        listeners: {
        	itemclick:{        		
        		fn:function(evt, rec){        	
        			log.debug("Clicked literature!", arguments)
        		}
        	},        	      
        	itemmouseenter:function(view, row){
        		mygraph.highlight( row.data._id, true)
        	},
        	itemmouseleave:function(view, row){
        		mygraph.highlight( row.data._id, false)
        	}
        },        	
        plugins: [ {
        	ptype:'rowexpander',
        	rowBodyTpl:[
        	 '<b>Authors</b>: {authors}<br>',
        	 '<b>Abstract:</b><br>{abstract}'
        	]	
        }],
        highlight:function(pubids, on){
        	for(var i=0;i<this.getStore().count();i++)
        		this.getView().removeRowCls(index, 'state-highlight')
        	for(var i=0;i<pubids.length;i++){        		
        		pubid = pubids[i]
        		if(pubid.indexOf("publ")<0) pubid = 'publ'+ pubid
        		var index = this.getStore().find('_id', pubid)
        		if(index>=0 && on)
        			this.getView().addRowCls(index, 'state-highlight')
        		if(index>=0 && !on)
        			this.getView().removeRowCls(index, 'state-highlight')
        	}
        }
    });


*/
 
 