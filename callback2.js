var selected_indices = source.selected.indices;
var data = source.data;
var selected_gkz = data['selected_gkz'];
var gkz = data['gkz'];


// Iterate over selected indices
for (var i = 0; i < selected_indices.length; i++) {
    var index = selected_indices[i];
    var current_gkz = gkz[index];
    const MAX_SELECTED_ITEMS = 132;
    
    // Toggle the selection status
    if (selected_gkz.includes(current_gkz)) {
        // If already selected, remove it
        selected_gkz.splice(selected_gkz.indexOf(current_gkz), 1);
        if(selected_gkz.length < MAX_SELECTED_ITEMS){
            selected_gkz.push('');
        }
        data['fill_color'][index] = "#d2b48c"; // Reset to blue
        console.log("unselected");
    } else {
        // If not selected, add it
        selected_gkz.push(current_gkz);
        if(selected_gkz.length >= MAX_SELECTED_ITEMS){
            selected_gkz.shift();
        }
        data['fill_color'][index] = "#ff0000"; // Set to red
        console.log("selected");
    }

}


console.log('Selected GKZ: ', selected_gkz)
// Update the data source
source.data = data;
source.change.emit();
/*
source2.data2 = data2;
source2.change.emit();
*/