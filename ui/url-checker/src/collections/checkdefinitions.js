import { List, Create, Edit, Datagrid, SimpleForm, required, SingleFieldList } from "react-admin";
import {TextInput, NumberInput, UrlField, NumberField, TextField, ReferenceManyField } from "react-admin";
import { CreateButton, EditButton, DeleteButton, Filter } from "react-admin";

const DefinitionFilter = (props) => (
    <Filter {...props}>
        <TextInput label="Search" source='urlcontains' alwaysOn />
    </Filter>
)

export const CheckDefinitionList = (props) => (
    <List {...props} filters={<DefinitionFilter/>}>
        <Datagrid rowClick="edit">
            <NumberField source="id" />
            <UrlField source="url" label='URL'/>
            <NumberField source="frequency" />
            <NumberField source="expectedStatus" />
            <TextField source="expectedString" />
            <ReferenceManyField label='E-mail Addresses' reference='notificationaddresses' target="checkId">
                <SingleFieldList>
                    <TextField source='emailAddress' />
                </SingleFieldList>
            </ReferenceManyField>
        </Datagrid>
    </List>
);

export const CheckDefinitionEdit = (props) => (
    <Edit {...props} title="Edit URL Check Definition">
        <SimpleForm>
            <TextInput source="url" label="URL" validate={required()} type='url'/>
            <NumberInput source="frequency" validate={required()}/>
            <NumberInput source="expectedStatus" validate={required()}/>
            <TextInput source="expectedString" />
            <ReferenceManyField label='E-mail Addresses' reference='notificationaddresses' target="checkId">
                <Datagrid>
                    <TextField source='emailAddress' />
                    <EditButton />
                    <DeleteButton />
                </Datagrid>
            </ReferenceManyField>
            <CreateButton basePath="/notificationaddresses" label="Add a new e-mail address" />
        </SimpleForm> 
    </Edit>
);

export const CheckDefinitionCreate = (props) => (
    <Create {...props} title="Create new URL Check Definition">
        <SimpleForm>
            <TextInput source="url" label="URL" validate={required()} type='url'/>
            <NumberInput source="frequency" validate={required()}/>
            <NumberInput source="expectedStatus" validate={required()}/>
            <TextInput source="expectedString" />
        </SimpleForm> 
    </Create>
);
