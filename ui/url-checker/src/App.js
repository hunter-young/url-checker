import * as React from "react";
import { Admin, Resource } from "react-admin";
import { CheckDefinitionList, CheckDefinitionEdit, CheckDefinitionCreate} from "./collections/checkdefinitions"
import { LatestResultList } from "./collections/latestresults"
import { NotificationAddressCreate, NotificationAddressEdit, NotificationAddressList} from "./collections/notificationadddresses"
import { CheckResultList } from "./collections/checkresults"
import jsonServerProvider from 'ra-data-json-server';
import NotificationsActiveIcon from '@material-ui/icons/NotificationsActive';
import TuneIcon from '@material-ui/icons/Tune';
import EmailIcon from '@material-ui/icons/Email';

const dataProvider = jsonServerProvider(window.location.origin)
const App = () => (
    <Admin dataProvider={dataProvider}>
        <Resource name="latestresults" 
            list={LatestResultList} 
            options={{ label: 'Latest Results'}} 
            icon={NotificationsActiveIcon} />
        <Resource name="checkdefinitions" 
            list={CheckDefinitionList} 
            edit={CheckDefinitionEdit} 
            create={CheckDefinitionCreate} 
            options={{ label: 'URL Checks'}} 
            icon={TuneIcon}/>
        <Resource name="notificationaddresses" 
            list={NotificationAddressList} 
            edit={NotificationAddressEdit} 
            create={NotificationAddressCreate} 
            options={{ label: 'E-mails'}} 
            icon={EmailIcon}/>
        <Resource name="checkresults" list={CheckResultList} 
            options={{ label: 'Results'}}/>
    </Admin>
);
export default App;