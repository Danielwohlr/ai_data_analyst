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


const DataTable = () => {

    const data = [
        [
            "INV001", "Paid", "$250.00", "Credit Card",
        ],
        [
            "INV001", "Paid", "$250.00", "Credit Card",
        ],
        [
            "INV001", "Paid", "$250.00", "Credit Card",
        ],
        [
            "INV001", "Paid", "$250.00", "Credit Card",
        ],
        [
            "INV001", "Paid", "$250.00", "Credit Card",
        ],
        [
            "INV001", "Paid", "$250.00", "Credit Card",
        ],
        [
            "INV001", "Paid", "$250.00", "Credit Card",
        ],
    ]

    const labels = ["Invoice", "Status", "Method", "Amount"]

    return (
        <Table>
            <TableHeader>
                <TableRow>
                    {labels.map((label, key) => (
                        <TableHead key={key}>{label}</TableHead>
                    ))}
                </TableRow>
            </TableHeader>
            <TableBody>
                {data.map((row, key) => (
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
