var groupingFeature = Ext.create('Ext.grid.feature.Grouping', {
	    groupHeaderTpl: '<input type="checkbox" name="filterByGroup" group="{name}" checked> Group: {name} ({rows.length})', //print the number of items in the group
	    startCollapsed: false // start all groups collapsed	  
	});


Ext.define('Precon.view.NetworkGrid' ,{
    extend: 'Ext.grid.Panel',
    requires: [
        //'Ext.selection.CheckboxModel'
    ],
    //selModel: Ext.create('Ext.selection.CheckboxModel'),
    features: [groupingFeature],
    alias : 'widget.networkgrid',
    id:'network-grid',
    title : 'Networks in Graph',
	
	//define the data
	store: 'Networks',
	
	constructor: function(config) {
			//this.initConfig(config);
			return this.callParent(arguments);
	}, 
	listeners:{
		click:{
			element:'el',
			fn: function(view, target){	
				if(target && target.type == 'checkbox' && target.name.indexOf('filter')==0 )
					filterNetwork(target, groupingFeature)  				
			}
		}
	},
    initComponent: function() {
              this.columns = [
								{
								    text     : '<input type=checkbox name="filterAll" checked> All', 
								    width    : 60, 
								    sortable : false, 
								    renderer : function(val,meta, record) {                				
								    				 return "<input class='filterByNetwork' belongtogroup='" + record.get("group") +"' type=checkbox "+ (val?"checked":"")+ " name='filterByNetwork' value='"+  record.get("_id") + "'>"
								    },
								    dataIndex: 'include'
								},
								{
								    text     : 'Network',
								    flex     : 1,
								    sortable : true,                 
								    dataIndex: 'name',
								    renderer: function(val, meta, record){
								    	return "<span class='clickable'>"+ val+"</a>"
								    }
								},
								{
								    text     : 'Creator', 
								    width    : 70, 
								    sortable : true, 
								    dataIndex: 'owner'
								   // renderer: change
								},
								{
								    text     : 'Source', 
								    width    : 75, 
								    flex:1,
								    sortable : true, 
								    dataIndex: 'source'
								   // renderer: change
								}
                          ];
     
              this.callParent(arguments);
    },
    highlight:function(ids, on){
    	for(var i=0;i<this.getStore().count();i++)
    		this.getView().removeRowCls(i, 'state-highlight')
    	for(var i=0;i<ids.length;i++){        		
    		var id = ids[i]    		
    		var index = this.getStore().find('_id', id)
    		if(index>=0 && on)
    			this.getView().addRowCls(index, 'state-highlight')
    		if(index>=0 && !on)    			this.getView().removeRowCls(index, 'state-highlight')
    	}
    }
});