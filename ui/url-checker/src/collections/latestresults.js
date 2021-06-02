import { List, Datagrid, Filter} from "react-admin";
import { UrlField, NumberField, TextField, DateField, TextInput } from "react-admin";

const DefinitionFilter = (props) => (
    <Filter {...props}>
        <TextInput label="Search" source='urlcontains' alwaysOn />
    </Filter>
)

export const LatestResultList = (props) => (
    <List {...props} title='Latest Results' filters={<DefinitionFilter />}>
        <Datagrid>
            <UrlField source="url" label="URL"/>
            <NumberField source="frequency" unit='second' />
            <NumberField source="expectedStatus" />
            <TextField source="expectedString" emptyText='None'/>
            <DateField source="lastChecked" showTime="true" />
            <TextField source="lastState" />
        </Datagrid>
    </List>
);
