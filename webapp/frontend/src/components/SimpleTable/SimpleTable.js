import React from 'react';
import {makeStyles} from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import {MdSignalCellular4Bar, MdSignalCellularOff} from 'react-icons/md'

const useStyles = makeStyles({
    table: {
        minWidth: 650,
    },
});

function createData(id, available) {
    return {id, available};
}

function returnAvailableIcon(available) {
    if (available) {
        return <MdSignalCellular4Bar style={{color: 'green'}}/>
    } else {
        return <MdSignalCellularOff style={{color: 'red'}}/>
    }
}

function buildSiteList(sites) {
    if (sites.sites !== undefined) {
        sites = sites.sites
        let siteRows = [];
        for (let i = 0; i < sites.length; i++) {
            let site = sites[i]
            let data = createData('Site ' + site.site_id, site.available)
            siteRows.push(data)
        }
        return siteRows
    } else {
        return []
    }
}

export default function SimpleTable(sites) {
    const classes = useStyles();
    const [selected, setSelected] = React.useState([]);
    const rows = buildSiteList(sites.sites)

    const handleClick = (event, id) => {
        const selectedIndex = selected.indexOf(id);
        let newSelected = [];
        if (selectedIndex === -1) {
            newSelected = newSelected.concat(selected, id);
        } else if (selectedIndex === 0) {
            newSelected = newSelected.concat(selected.slice(1));
        } else if (selectedIndex === selected.length - 1) {
            newSelected = newSelected.concat(selected.slice(0, -1));
        } else if (selectedIndex > 0) {
            newSelected = newSelected.concat(
                selected.slice(0, selectedIndex),
                selected.slice(selectedIndex + 1),
            );
        }
        setSelected(newSelected);
    };

    const isSelected = name => selected.indexOf(name) !== -1;

    return (
        <TableContainer component={Paper}>
            <Table className={classes.table} aria-label="simple table">
                <TableHead>
                    <TableRow>
                        <TableCell>Site ID</TableCell>
                        <TableCell align="right">Available</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {rows.map(row => {
                        const isItemSelected = isSelected(row.id);
                        return (
                            <TableRow
                                key={row.id}
                                selected={isItemSelected}
                                onClick={event => handleClick(event, row.id)}>
                                <TableCell component="th" scope="row">
                                    {row.id}
                                </TableCell>
                                <TableCell align="right">{returnAvailableIcon(row.available)}</TableCell>
                            </TableRow>)
                    })}
                </TableBody>
            </Table>
        </TableContainer>
    );
}