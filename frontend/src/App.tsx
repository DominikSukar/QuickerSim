import { useEffect, useState } from "react";
import "./App.css";
import Box from "@mui/material/Box";
import { DataGrid, GridColDef, GridRenderCellParams } from "@mui/x-data-grid";
import { Button, ToggleButton, ToggleButtonGroup } from "@mui/material";
import axios from "axios";
import FormModal from "./components/Modal";
import { Unit, kgToLbs } from "./utils/unitConversion";

interface RowData {
  id: number;
  date: string;
  mass: string;
}

function App() {
  const [rows, setRows] = useState<RowData[]>([]);
  const [open, setOpen] = useState(false);
  const [isEdit, setIsEdit] = useState(false);
  const [formData, setFormData] = useState({ date: "", mass: "" });
  const [displayUnit, setDisplayUnit] = useState<Unit>("kg");

  const handleDelete = async (date: string) => {
    try {
      await axios.delete(`http://localhost:8000/readings/${date}`);
      fetchData();
    } catch (error) {
      console.error("Error deleting reading:", error);
    }
  };

  const handleOpenForPut = (reading: {
    id: number;
    date: string;
    mass: number;
  }) => {
    const date = reading.date;
    setIsEdit(true);
    setFormData((prevData) => ({ ...prevData, date }));
    setOpen(true);
  };

  const handleUnitChange = (
    _event: React.MouseEvent<HTMLElement>,
    newUnit: Unit
  ) => {
    if (newUnit !== null) {
      setDisplayUnit(newUnit);
    }
  };

  const formatMass = (mass: string) => {
    const numMass = parseFloat(mass);
    const convertedMass = displayUnit === "lbs" ? kgToLbs(numMass) : numMass;
    return `${convertedMass.toFixed(1)} ${displayUnit}`;
  };

  const columns: GridColDef<RowData>[] = [
    { field: "id", headerName: "ID", width: 90 },
    {
      field: "date",
      headerName: "Date",
      width: 150,
      editable: true,
    },
    {
      field: "mass",
      headerName: `Mass (${displayUnit})`,
      width: 150,
      editable: true,
      valueFormatter: (param: string) => formatMass(param),
    },
    {
      field: "actions",
      headerName: "Actions",
      width: 180,
      renderCell: (params: GridRenderCellParams) => (
        <div>
          <Button
            variant="contained"
            size="small"
            onClick={() => handleOpenForPut(params.row)}
            sx={{ mr: 1 }}
          >
            Edit
          </Button>
          <Button
            variant="contained"
            color="error"
            size="small"
            onClick={() => handleDelete(params.row.date)}
          >
            Delete
          </Button>
        </div>
      ),
    },
  ];

  const fetchData = async () => {
    try {
      const response = await axios.get<RowData[]>(
        "http://localhost:8000/readings/"
      );
      setRows(response.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ mb: 2, display: "flex", justifyContent: "space-between" }}>
        <FormModal
          open={open}
          setOpen={setOpen}
          isEdit={isEdit}
          setIsEdit={setIsEdit}
          formData={formData}
          setFormData={setFormData}
          onSuccess={fetchData}
          displayUnit={displayUnit}
        />
        <ToggleButtonGroup
          value={displayUnit}
          exclusive
          onChange={handleUnitChange}
          aria-label="mass unit"
        >
          <ToggleButton value="kg" aria-label="kilograms">
            kg
          </ToggleButton>
          <ToggleButton value="lbs" aria-label="pounds">
            lbs
          </ToggleButton>
        </ToggleButtonGroup>
      </Box>
      <Box sx={{ height: 400, width: "100%" }}>
        <DataGrid
          rows={rows}
          columns={columns}
          initialState={{
            sorting: {
              sortModel: [{ field: "date", sort: "desc" }],
            },
            pagination: {
              paginationModel: {
                pageSize: 5,
              },
            },
          }}
          pageSizeOptions={[5]}
          disableRowSelectionOnClick
        />
      </Box>
    </Box>
  );
}

export default App;