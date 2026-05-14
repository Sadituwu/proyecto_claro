import { HomeFilled, Tickets, User, Setting, Avatar, FolderOpened, DataAnalysis , List } from '@element-plus/icons-vue'

export const menuItems = [

    { title: 'Modelo', icon: DataAnalysis , routeName: '/modelo', roles: ['admin', 'client', 'support'] },
    { title: 'Registro', icon: List  , routeName: '/registro', roles: ['admin', 'client', 'support'] },

];

export default menuItems;
