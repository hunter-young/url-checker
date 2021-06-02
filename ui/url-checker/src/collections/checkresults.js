import { List, Datagrid, UrlField, NumberField, TextField, DateField } from "react-admin";

export const CheckResultList = (props) => (
    <List {...props}>
        <Datagrid>
            <UrlField source="checkDefinition.url" label='Check URL'/>
            <DateField source="timeChecked" showTime="true" />
            <NumberField source="statusCode" />
            <TextField source="state" />
            <TextField source="id" />            
        </Datagrid>
    </List>
);