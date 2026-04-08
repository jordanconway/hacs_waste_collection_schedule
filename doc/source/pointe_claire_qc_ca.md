# Pointe-Claire (QC)

Waste collection schedules for the [City of Pointe-Claire](https://www.pointe-claire.ca), Québec, Canada.

## Configuration via configuration.yaml

```yaml
waste_collection_schedule:
  sources:
    - name: pointe_claire_qc_ca
      args:
        sector: SECTOR
```

### Configuration Variables

**SECTOR**
*(string) (required)*

Your collection sector — either `A` or `B`.

#### How do I find my sector?

Visit the [City of Pointe-Claire waste management page](https://www.pointe-claire.ca/en/residents/public-works/waste-management/) to determine which sector applies to your address.

## Collection Types

| Type | Description |
|------|-------------|
| Organic Waste | Weekly — every Monday |
| Recyclables | Weekly — every Wednesday (blue box) |
| Household Waste | Bi-weekly — every second Tuesday (Sector A) or every second Thursday (Sector B) |
| Bulky Items | Monthly — first Wednesday of each month |
| Christmas Tree Collection | Special pickup in early January |

## Example

```yaml
waste_collection_schedule:
  sources:
    - name: pointe_claire_qc_ca
      calendar_title: Pointe-Claire Waste Collection
      args:
        sector: A
```
