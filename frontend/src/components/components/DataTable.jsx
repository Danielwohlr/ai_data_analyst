import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableFooter,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"


const DataTable = ({ content }) => {

    if (!content) {
        return <div>Loading chart data...</div>;
    }

    return (
        <Table>
            <TableHeader>
                <TableRow>
                    {content.labels.map((label, key) => (
                        <TableHead key={key}>{label}</TableHead>
                    ))}
                </TableRow>
            </TableHeader>
            <TableBody>
                {content.data.map((row, key) => (
                    <TableRow key={key}>
                        {row.map((value, key) => (
                            <TableCell key={key}>{value}</TableCell>
                        ))}
                    </TableRow>
                ))}
            </TableBody>
        </Table>
    )
}

export default DataTable;
