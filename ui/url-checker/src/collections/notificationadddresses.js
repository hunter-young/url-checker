import { List, Edit, Create,Datagrid, SimpleForm, required } from "react-admin";
import { TextField, ReferenceField, SelectInput, TextInput, ReferenceInput } from "react-admin";

export const NotificationAddressList = (props) => (
    <List {...props}>
        <Datagrid rowClick="edit">
            <ReferenceField source="checkId" label='URL Check' reference="checkdefinitions">
                <TextField source="url" />
            </ReferenceField>
            <TextField source="emailAddress" />
            <TextField source="id" />
        </Datagrid>
    </List>
);

export const NotificationAddressEdit = (props) => (
    <Edit {...props} title="Edit Notification E-mail Address">
        <SimpleForm>
            <ReferenceField source="checkId" label='URL Check' reference="checkdefinitions">
                <TextField source="url" />
            </ReferenceField>
            <TextInput source='emailAddress' label='E-mail Address' validate={required()} />
        </SimpleForm> 
    </Edit>
);

export const NotificationAddressCreate = (props) => (
    <Create {...props} title="Create new Notification E-mail">
        <SimpleForm>
            <ReferenceInput source="checkId" label='URL Check' reference="checkdefinitions">
                <SelectInput optionText='url' />
            </ReferenceInput>
            <TextInput source='emailAddress' label='E-mail Address' validate={required()} />
        </SimpleForm> 
    </Create>
);