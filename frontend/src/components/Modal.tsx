import React, { useState } from "react";
import {
  Button,
  Modal,
  Box,
  TextField,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
} from "@mui/material";
import axios from "axios";
import { Unit, lbsToKg } from "../utils/unitConversion";

interface FormModalProps {
  open: boolean;
  setOpen: (open: boolean) => void;
  isEdit: boolean;
  setIsEdit: (open: boolean) => void;
  formData: { date: string; mass: string };
  setFormData: (formData: { date: string; mass: string }) => void;
  onSuccess: () => void;
  displayUnit: Unit;
}

interface ValidationErrors {
  date?: string;
  mass?: string;
}

const FormModal: React.FC<FormModalProps> = ({
  open,
  setOpen,
  isEdit,
  setIsEdit,
  formData,
  setFormData,
  onSuccess,
  displayUnit,
}) => {
  const [unit, setUnit] = useState<Unit>(displayUnit);
  const [errors, setErrors] = useState<ValidationErrors>({});
  const [submitError, setSubmitError] = useState<string | null>(null);

  const handleClose = () => {
    setOpen(false);
    setErrors({});
    setSubmitError(null);
  };

  const handleOpen = () => {
    setIsEdit(false);
    setOpen(true);
    setFormData({ date: "", mass: "" });
    setUnit(displayUnit);
  };

  const validateForm = (): boolean => {
    const newErrors: ValidationErrors = {};

    if (!formData.date) {
      newErrors.date = "Date is required";
    } else if (!isEdit && !/^\d{4}-\d{2}-\d{2}$/.test(formData.date)) {
      newErrors.date = "Invalid date format (YYYY-MM-DD)";
    }

    const massNum = parseFloat(formData.mass);
    if (!formData.mass) {
      newErrors.mass = "Mass is required";
    } else if (isNaN(massNum) || massNum <= 0) {
      newErrors.mass = "Mass must be a positive number";
    } else if (massNum > 1000) {
      newErrors.mass = "Mass seems too high";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setErrors((prev) => ({ ...prev, [e.target.name]: undefined }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitError(null);

    if (!validateForm()) {
      return;
    }

    try {
      const massInKg =
        unit === "lbs"
          ? lbsToKg(parseFloat(formData.mass))
          : parseFloat(formData.mass);

      const dataToSubmit = {
        ...formData,
        mass: massInKg.toFixed(1),
      };

      if (isEdit) {
        await axios.put(
          `http://localhost:8000/readings/${formData.date}/`,
          dataToSubmit
        );
      } else {
        await axios.post("http://localhost:8000/readings/", dataToSubmit);
      }

      onSuccess();
      handleClose();
    } catch (error: any) {
      setSubmitError(
        error.response?.data?.detail || "Error submitting form. Please try again."
      );
    }
  };

  return (
    <div>
      <Button variant="contained" color="primary" onClick={handleOpen}>
        ADD
      </Button>
      <Modal open={open} onClose={handleClose}>
        <Box sx={{ ...modalStyle }}>
          <Typography variant="h6" component="h2" sx={{ mb: 2 }}>
            {isEdit ? "Edit Reading" : "Add New Reading"}
          </Typography>
          <form onSubmit={handleSubmit}>
            {!isEdit && (
              <TextField
                label="Date"
                name="date"
                type="date"
                value={formData.date}
                onChange={handleChange}
                fullWidth
                margin="normal"
                InputLabelProps={{ shrink: true }}
                error={!!errors.date}
                helperText={errors.date}
              />
            )}
            <TextField
              label="Mass"
              name="mass"
              type="number"
              value={formData.mass}
              onChange={handleChange}
              fullWidth
              margin="normal"
              error={!!errors.mass}
              helperText={errors.mass}
            />
            <FormControl fullWidth margin="normal">
              <InputLabel>Unit</InputLabel>
              <Select
                value={unit}
                label="Unit"
                onChange={(e) => setUnit(e.target.value as Unit)}
              >
                <MenuItem value="kg">Kilograms (kg)</MenuItem>
                <MenuItem value="lbs">Pounds (lbs)</MenuItem>
              </Select>
            </FormControl>

            {submitError && (
              <Alert severity="error" sx={{ mt: 2, mb: 2 }}>
                {submitError}
              </Alert>
            )}

            <Box sx={{ mt: 2, display: "flex", justifyContent: "flex-end" }}>
              <Button
                onClick={handleClose}
                variant="outlined"
                sx={{ mr: 1 }}
              >
                Cancel
              </Button>
              <Button type="submit" variant="contained" color="primary">
                {isEdit ? "Update" : "Submit"}
              </Button>
            </Box>
          </form>
        </Box>
      </Modal>
    </div>
  );
};

const modalStyle = {
  position: "absolute" as const,
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 400,
  bgcolor: "background.paper",
  boxShadow: 24,
  p: 4,
  borderRadius: 1,
};

export default FormModal;