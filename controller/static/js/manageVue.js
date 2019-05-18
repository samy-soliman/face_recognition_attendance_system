new Vue({
    el: '#vue-app',
    data: {
        selectedEntity: "",
        selectedAction: "",

    },
    methods: {
        changeSelectedEntity(option) {
            this.selectedEntity = option
        },
        changeSelectedAction(option) {
            this.selectedAction = option
        },
        checkSelected(caller) {
            // Instructor 
            // caller == Delete 1 ------ Add 2
           if (this.selectedEntity == "Instructor") {
                if(this.selectedAction=="Delete")
                {
                    if(caller =="1")
                        return true;
                }
                else if(this.selectedAction=="Add")
                {
                    if(caller =="2")
                        return true;
                }
            }
            // Courses 
            // caller == Delete 3 ------ Add 4
            else if (this.selectedEntity == "Courses") {
                if(this.selectedAction=="Delete")
                {
                    if(caller =="3")
                        return true;
                }
                else if(this.selectedAction=="Add")
                {
                    if(caller =="4")
                        return true;
                }
            }
            // Student 
            // caller == Delete 5 ------ Add 6
            else  if (this.selectedEntity == "Student") {
                if(this.selectedAction=="Delete")
                {
                    if(caller =="5")
                        return true;
                }
                else if(this.selectedAction=="Add")
                {
                    if(caller =="6")
                        return true;
                }
            }
            else{
                return false ;
            }
        }
    }
})