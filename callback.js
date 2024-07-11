const callback = function(cb_obj){
    const indices = cb_obj.indices;
    const data = source.data;
    let selected_indices = data['selected_indices'];
    let selected_gkz = data['selected_gkz'];
        
    /*Toggle selection state of clicked indices          <----- Version 1
    for(let i =0; i<indices.length; i++){
        const index = indices[i];
        const selected_index = selected_indices.indexOf(index);
        if(selected_index == -1){
            selected_indices.push(index)
            selected_gkz.push(data['gkz'][index]);
        }else{
            selected_indices.splice(selected_index, 1);
            selected_gkz.splice(selected_index, 1);
       }
      } */               
    indices.forEach((index) => {
        const selected_index = selected_indices.indexOf(index);
        if(selected_index === -1){
            selected_indices.push(index);
            selected_gkz.push(data['gkz'][index]);
        }else{
            selected_indices.splice(selected_index, 1);
            selected_gkz.splice(selected_index, 1);
        }
    });
    //Reset all colors and widths
    for (let i = 0; i<data['x'].length, i++;){
        data['line_color'][i] = 'white';
        data['line_width'][i] = 0.5;
    }
    //Apply selcetion colors and widths             <---- Version 1
    //for(let i = 0; i < selected_indices.length; i++){
      //  const selected_index = selected_indices[i];
        //data['line_color'][selected_index] = 'yellow';
        //data['line_width'][selected_index] = 2;
    //}
    selected_indices.forEach((index)=>{
        data['line_color'][index] = 'yellow';
        data['line_width'][index] = 2;
    });
    console.log('Ausgewählte GKZ:',selected_gkz);
    source.change.emit();
    //source.change('trigger')
};