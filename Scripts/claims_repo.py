@app.task()
def claim_reports(context, report_id, report_obj_of):
    if report_obj_of == "Dealer":
        reportObj = DealerReport.objects.get(id=report_id)
    else:
        reportObj = Report.objects.get(id=report_id)

    user_id = context.get("user", 0)
    company_id = context.get("company_id", 0)
    is_super_admin = context.get("is_super_admin", None)
    external_admin = context.get("external_admin", None)
    dealer_ids = context.get("dealer", None)
    reinsurances = context.get("reinsurances", None)
    claim_start_date = context.get("claim_start_date", None)
    claim_end_date = context.get("claim_end_date", None)
    agreement_start_date = context.get("agreement_start_date", None)
    agreement_end_date = context.get("agreement_end_date", None)

    if report_obj_of == "Dealer":
        report_description = "Claim Reports"
    else:
        reportObj.section = ReportSection.CLAIM_REPORTS

    try:
        user = User.objects.get(id=user_id)
    except Exception as ex:
        if report_obj_of != "Dealer":
            report_description = "Invalid user request"
        exception_message(reportObj, ProgressStatus.ERROR, report_description, str(ex))
        return
    try:
        companyObj = Company.cache.get(id=int(company_id))
    except Company.DoesNotExist as ex:
        companyObj = None
        if report_obj_of != "Dealer":
            report_description = "Invalid company request"
        exception_message(reportObj, ProgressStatus.ERROR, report_description, str(ex))
        return

    reportObj.status = ProgressStatus.INPROGRESS
    reportObj.user = user
    reportObj.company = companyObj
    reportObj.save()
    
    dealers = Dealer.objects.filter(id__in=dealer_ids)
    for dealer in dealers:
        claim_filter = {
                "dealer__company__id": dealer.company.id,
                "dealer__id": dealer_ids,
            }
        claim_from_date = "ALL"
        claim_to_date = "ALL"
        agreement_from_date = "ALL"
        agreement_to_date = "ALL"
        
        if claim_start_date is not None and claim_start_date != '':
            claim_filter["date__gte"] = claim_start_date
            claim_from_date = claim_start_date

        if claim_end_date is not None and claim_end_date != '':
            claim_filter["date__lte"] = claim_end_date
            claim_to_date = claim_end_date

        if agreement_start_date is not None and agreement_start_date != '':
            claim_filter["agreement__purchased_date__gte"] = agreement_start_date
            agreement_from_date = agreement_start_date

        if agreement_end_date is not None and agreement_end_date != '':
            claim_filter["agreement__purchased_date__lte"] = agreement_end_date
            agreement_to_date = agreement_end_date
            
        if reinsurances is not None and reinsurances != [] and reinsurances != "" and reinsurances != 0:
            claim_filter["agreement__reinsurance__id__in"] = reinsurances
            
        if is_super_admin is False:
            claim_filter["agreement__dealer__external_admin__id"] = external_admin

        workbook = Workbook()
        std = workbook['Sheet']
        workbook.remove(std)

        # Generate random start and end colors
        # start_color = f"{random.randint(0, 255):02X}{random.randint(0, 255):02X}{random.randint(0, 255):02X}"
        # end_color = f"{random.randint(0, 255):02X}{random.randint(0, 255):02X}{random.randint(0, 255):02X}"

        # Create a gradient fill pattern
        gradient_fill = PatternFill(start_color="1dab45", end_color="1dab45", fill_type="solid")

        paid = workbook.create_sheet('Paid Claims')
        approved = workbook.create_sheet('Approved Not Paid')
        unapproved = workbook.create_sheet('Pending Not Approved')

        all_claim_sheets = [
            ("paid", paid),
            ("approved", approved),
            ("unapproved", unapproved),
            ]
        
        for claim_sheets in all_claim_sheets:
            sheet_name = claim_sheets[0]
            claim_sheet = claim_sheets[1]
            
            if sheet_name == "paid":
                claim_filter["admin_paid"] = True
                claim_sheet.cell(row=1, column=5).value = 'Claims Report'
                claim_sheet.cell(row=2, column=2).value = 'Paid Claims'
            elif sheet_name == "approved":
                claim_filter["admin_paid"] = False
                claim_filter["approve"] = True
                claim_sheet.cell(row=1, column=5).value = 'Pending Claims Report'
                claim_sheet.cell(row=2, column=2).value = 'Approved Not Paid'
            else:
                claim_filter["admin_paid"] = False
                claim_filter["approve"] = False
                claim_sheet.cell(row=1, column=5).value = 'Pending Claims Report'
                claim_sheet.cell(row=2, column=2).value = 'Filed Not Approved'

            # main report heading
            claim_sheet.merge_cells(start_row=1, start_column=5, end_row=1, end_column=7)
            claim_sheet.cell(row=1, column=5).font = Font(size=18, bold=True)
            claim_sheet.cell(row=1, column=5).alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

            # 2nd report heading
            claim_sheet.merge_cells(start_row=2, start_column=2, end_row=2, end_column=5)
            claim_sheet.cell(row=2, column=2).font = Font(size=18, bold=True)
            claim_sheet.cell(row=2, column=2).alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

            claim_sheet.cell(row=3,column=2).value = 'Company'
            claim_sheet.cell(row=3,column=3).value = dealer.company.name
            claim_sheet.cell(row=4,column=2).value = 'Dealer'
            claim_sheet.cell(row=4,column=3).value = dealer.name
            claim_sheet.cell(row=4,column=4).value = dealer.dealer_number
            
            reinsurances_name = ReInsurance.objects.filter(id__in=reinsurances).values_list('name', flat=True)
            claim_sheet.cell(row=5,column=2).value = 'Reinsurance'
            claim_sheet.cell(row=5,column=3).value = str(list(reinsurances_name)).replace('[', '').replace(']', '') if reinsurances_name else "ALL"
            
            claim_sheet.cell(row=6,column=2).value = 'Claim Start'
            claim_sheet.cell(row=6,column=3).value = str(claim_from_date)
            claim_sheet.cell(row=7,column=2).value = 'Claim End'
            claim_sheet.cell(row=7,column=3).value = str(claim_to_date)
            claim_sheet.cell(row=8,column=2).value = 'Agreement Start'
            claim_sheet.cell(row=8,column=3).value = str(agreement_from_date)
            claim_sheet.cell(row=9,column=2).value = 'Agreement End'
            claim_sheet.cell(row=9,column=3).value = str(agreement_to_date)
            claim_sheet.cell(row=10,column=2).value = 'Created at'
            claim_sheet.cell(row=10,column=3).value = timezone.now().strftime("%m/%d/%Y")

            row_index = 11
            
            claim_header = [
                "Dealership",
                "ClaimDate",
                "Claim",
                "SubPlan",
                "Vin",
                "Customer",
                "Part Cost",
                "Claim Type",
                "Component",
                "Labour Hours",
                "Labour Cost",
                "Miles Driven",
                "Elapsed Time",
                "Repiar Done By",
                "Total Claim",
                "Net Cost",
                "Inspection fee",
                "Paid by",
                "Filed By",
            ]
            
            claim_sheet.append([])
            for header_item in claim_header:
                cell = claim_sheet.cell(row=row_index, column=claim_header.index(header_item) + 1, value=header_item)
                cell.font = Font(size=12, bold=True)
                cell.fill = gradient_fill
            total_parts_cost = 0
            total_labour_hours = 0
            total_labour_cost = 0
            total_total_claim = 0
            total_net_cost = 0
            
            data = {}
            claims = CustomerClaim.objects.filter(**claim_filter)
            for claim in claims:
                row_index += 1
                agreement = claim.agreement
                claim_paid_amount = round(claim.total_paid + claim.diagnostic_fee, 2)
                cal_part_cost = claim.cal_part_cost()
                get_type_of_claim_components = claim.get_type_of_claim_components
                cal_labor_hour = claim.cal_labor_hour()
                cal_labor_cost = claim.cal_labor_cost()
                miles_driven = claim.miles_driven()
                elapsed_time = claim.elapsed_time()
                repair_done_by = claim.repair_done_by()

                subplan = agreement.SubPlan
                claim_type = claim.claim_type
                if claim_type is None:
                    claim_type = agreement.agreement_type
                if claim_type == AGREEMENTCHOICES.DEBT_CANCELLATION:
                    claim_type = "debt"
                elif claim_type == AGREEMENTCHOICES.MAINTENANCE:
                    claim_type = "maint"
                data_list = [
                    claim.dealer.name,
                    claim.date.strftime("%m/%d/%Y"),
                    claim.claim_number,
                    agreement.SubPlan,
                    agreement.VIN,
                    agreement.customer_name,
                    cal_part_cost,
                    claim_type,
                    get_type_of_claim_components,
                    cal_labor_hour,
                    cal_labor_cost,
                    miles_driven,
                    elapsed_time,
                    repair_done_by,
                    claim_paid_amount,
                    claim.net_total,
                    claim.inspection_fee,
                    claim.paid_by,
                    claim.filled_by.name if claim.filled_by else "Not found"
                ]

                # for adjust I column only
                adjusted_width = len(get_type_of_claim_components)/2 if len(get_type_of_claim_components) > 50 else len(get_type_of_claim_components)+50
                claim_sheet.column_dimensions['I'].width = adjusted_width
                claim_sheet.column_dimensions['F'].width = 25

                # # Apply the rich text string to a cell
                component_cell = claim_sheet.cell(row=row_index, column=9)
                component_cell.alignment = Alignment(vertical='top', wrapText=True)

                claim_sheet.append(data_list)
                
                total_parts_cost += cal_part_cost
                total_labour_hours += cal_labor_hour
                total_labour_cost += cal_labor_cost
                total_total_claim += claim.total
                total_net_cost += claim.net_total

                if claim_type in data.keys():
                    if subplan not in data[claim_type].keys():
                        data[claim_type][subplan] = [
                                    1,
                                    round(claim_paid_amount, 2),
                                    round(cal_part_cost, 2),
                                    round(cal_labor_hour, 2),
                                    int(miles_driven),
                                    int(elapsed_time),
                                    int(cal_labor_cost),
                                    0,
                                    0,
                                    0,
                                    0,
                                    0,
                                    0,
                                ]

                        # FOR EARLY CLAIMS
                        if (claim.date - agreement.purchased_date.date()).days < 35:
                            data[claim_type][subplan][7]  = 1
                            data[claim_type][subplan][8]  = round(cal_part_cost, 2)
                            data[claim_type][subplan][9]  = round(cal_labor_hour, 2)
                            data[claim_type][subplan][10] = int(miles_driven)
                            data[claim_type][subplan][11] = int((claim.date - agreement.purchased_date.date()).days)
                            data[claim_type][subplan][12] = int(cal_labor_cost)
                        
                    else:
                        data[claim_type][subplan][0] = data[claim_type][subplan][0] + 1
                        data[claim_type][subplan][1] = round(data[claim_type][subplan][1] + claim_paid_amount, 2)
                        data[claim_type][subplan][2] = round(data[claim_type][subplan][2] + cal_part_cost, 2)
                        data[claim_type][subplan][3] = round(data[claim_type][subplan][3] + cal_labor_hour, 2)
                        data[claim_type][subplan][4] = data[claim_type][subplan][4] + int(miles_driven)
                        data[claim_type][subplan][5] = data[claim_type][subplan][5] + int(elapsed_time)
                        data[claim_type][subplan][6] = data[claim_type][subplan][6] + int(cal_labor_cost)

                        # FOR EARLY CLAIMS
                        if (claim.date - agreement.purchased_date.date()).days < 35:
                            data[claim_type][subplan][7]  = data[claim_type][subplan][7] + 1
                            data[claim_type][subplan][8]  = data[claim_type][subplan][8] + round(cal_part_cost, 2)
                            data[claim_type][subplan][9]  = data[claim_type][subplan][9] + round(cal_labor_hour, 2)
                            data[claim_type][subplan][10] = data[claim_type][subplan][10] + int(miles_driven)
                            data[claim_type][subplan][11] = data[claim_type][subplan][11] + int((claim.date - agreement.purchased_date.date()).days)
                            data[claim_type][subplan][12] = data[claim_type][subplan][12] + int(cal_labor_cost)
                        
                else:
                    data[claim_type] = {subplan: []}
                    data[claim_type][subplan] = [
                        1, #  0: count
                        claim_paid_amount, # 1: paid amount
                        round(cal_part_cost, 2), # 2: avg part cost
                        round(cal_labor_hour, 2), # 3: avg labor hour
                        int(miles_driven), # 4: avg miles driven
                        int(elapsed_time), # 5: avg elapsed time
                        int(cal_labor_cost), # 6: avg labor cost
                        0, # 7: early count
                        0, # 8: early part cost
                        0, # 9: early labor hour
                        0, # 10: early miles driven
                        0, # 11: early elapsed time
                        0, # 12: early labor cost
                        ]
                    # FOR EARLY CLAIMS
                    if (claim.date - agreement.purchased_date.date()).days < 35:
                        data[claim_type][subplan][7]  = 1
                        data[claim_type][subplan][8]  = round(cal_part_cost, 2)
                        data[claim_type][subplan][9]  = round(cal_labor_hour, 2)
                        data[claim_type][subplan][10] = int(miles_driven)
                        data[claim_type][subplan][11] = int((claim.date - agreement.purchased_date.date()).days)
                        data[claim_type][subplan][12] = int(cal_labor_cost)

            # early claims divided by total number of claims 
            claim_sheet.append(["Total","","","","","", total_parts_cost,"","", total_labour_hours, total_labour_cost,"","","", total_total_claim, total_net_cost])
            for row in claim_sheet.iter_rows(min_row=claim_sheet.max_row, max_row=claim_sheet.max_row):
                for cell in row:
                    cell.alignment = Alignment(horizontal='left', vertical='top',wrap_text=True)
                    cell.font = Font(bold=True)

            row_index += 6
            summary_header_column_index = 1
            claim_sheet.cell(row=row_index, column=4).value = 'Summary'
            claim_sheet.cell(row=row_index, column=4).font = Font(size=18, bold=True)
            claim_sheet.cell(row=row_index, column=4).alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
            row_index += 1
            summary_row_index = row_index
            row_index += 1

            for summary_data_key, summary_data_val in data.items():
                cell = claim_sheet.cell(row=summary_row_index, column=summary_header_column_index)
                cell.value = summary_data_key
                cell.font = Font(size=14, bold=True)
                cell.fill = gradient_fill
                cell = claim_sheet.cell(row=summary_row_index, column=summary_header_column_index+1)
                cell.value = "Count"
                cell.font = Font(size=14, bold=True)
                cell.fill = gradient_fill
                cell = claim_sheet.cell(row=summary_row_index, column=summary_header_column_index+2)
                cell.value = "Amount"
                cell.font = Font(size=14, bold=True)
                cell.fill = gradient_fill

                summary_header_column_index += 4
                summany_data_column_index = summary_header_column_index - 4
                summany_data_row_index = row_index
                summany_average_row_index = row_index

                total_part_cost = 0
                total_labor_time = 0
                total_miles_lapsed = 0
                total_time_lapsed = 0
                total_labor_cost = 0

                total_claims = 0
                early_total = 0
                early_part_cost = 0
                early_labor_time = 0
                early_miles_lapsed = 0
                early_time_lapsed = 0
                early_labor_cost = 0


                for i, j in summary_data_val.items():
                    claim_sheet.cell(row=summany_data_row_index, column=summany_data_column_index).value = i
                    claim_sheet.cell(row=summany_data_row_index, column=summany_data_column_index+1).value = j[0]
                    claim_sheet.cell(row=summany_data_row_index, column=summany_data_column_index+2).value = j[1]

                    total_claims += j[0]
                    total_part_cost += j[2]
                    total_labor_time += j[3]
                    total_miles_lapsed += j[4]
                    total_time_lapsed += j[5]
                    total_labor_cost += j[6]

                    early_total += j[7]
                    early_part_cost += j[8]
                    early_labor_time += j[9]
                    early_miles_lapsed += j[10]
                    early_time_lapsed += j[11]
                    early_labor_cost += j[12]

                    summany_data_row_index += 1
                    summany_average_row_index += 1
                summany_data_row_index = row_index
                summany_data_column_index = summary_header_column_index

                summany_average_row_index += 2

                # averages 
                cell = claim_sheet.cell(row=summany_average_row_index, column=summany_data_column_index-4)
                cell.value = "Averages"
                cell.font = Font(size=12, bold=True)
                cell.fill = gradient_fill
                
                summany_average_row_index += 1
                claim_sheet.cell(row=summany_average_row_index, column=summany_data_column_index-4).value = "Part Cost"
                claim_sheet.cell(row=summany_average_row_index, column=summany_data_column_index-2).value = round(total_part_cost/total_claims, 2)
                summany_average_row_index += 1
                claim_sheet.cell(row=summany_average_row_index, column=summany_data_column_index-4).value = "Labor Time"
                claim_sheet.cell(row=summany_average_row_index, column=summany_data_column_index-2).value = round(total_labor_time/total_claims, 2)
                summany_average_row_index += 1
                claim_sheet.cell(row=summany_average_row_index, column=summany_data_column_index-4).value = "Labor Cost"
                claim_sheet.cell(row=summany_average_row_index, column=summany_data_column_index-2).value = round(total_labor_cost/total_claims, 2)
                summany_average_row_index += 1
                claim_sheet.cell(row=summany_average_row_index, column=summany_data_column_index-4).value = "Miles Lapsed"
                claim_sheet.cell(row=summany_average_row_index, column=summany_data_column_index-2).value = round(total_miles_lapsed/total_claims, 2)
                summany_average_row_index += 1
                claim_sheet.cell(row=summany_average_row_index, column=summany_data_column_index-4).value = "Time Lapsed"
                claim_sheet.cell(row=summany_average_row_index, column=summany_data_column_index-2).value = round(total_time_lapsed/total_claims, 2)
                summany_average_row_index += 1

                # early claims 
                summany_average_row_index += 1
                cell = claim_sheet.cell(row=summany_average_row_index, column=summany_data_column_index-4)
                cell.value = "Early Claims"
                cell.font = Font(size=12, bold=True)
                cell.fill = gradient_fill

                summany_average_row_index += 1
                claim_sheet.cell(row=summany_average_row_index, column=summany_data_column_index-4).value = "#"
                claim_sheet.cell(row=summany_average_row_index, column=summany_data_column_index-2).value = early_total
                summany_average_row_index += 1
                claim_sheet.cell(row=summany_average_row_index, column=summany_data_column_index-4).value = f"% of total"
                claim_sheet.cell(row=summany_average_row_index, column=summany_data_column_index-2).value = round((early_total/total_claims)*100, 2) if early_total > 0 else 0
                summany_average_row_index += 1
                claim_sheet.cell(row=summany_average_row_index, column=summany_data_column_index-4).value = "Part Cost"
                claim_sheet.cell(row=summany_average_row_index, column=summany_data_column_index-2).value = round(early_part_cost/early_total, 2) if early_total > 0 else 0
                summany_average_row_index += 1
                claim_sheet.cell(row=summany_average_row_index, column=summany_data_column_index-4).value = "Labor Time"
                claim_sheet.cell(row=summany_average_row_index, column=summany_data_column_index-2).value = round(early_labor_time/early_total, 2) if early_total > 0 else 0
                summany_average_row_index += 1
                claim_sheet.cell(row=summany_average_row_index, column=summany_data_column_index-4).value = "Labor Cost"
                claim_sheet.cell(row=summany_average_row_index, column=summany_data_column_index-2).value = round(early_labor_cost/early_total, 2) if early_total > 0 else 0
                summany_average_row_index += 1
                claim_sheet.cell(row=summany_average_row_index, column=summany_data_column_index-4).value = "Miles Lapsed"
                claim_sheet.cell(row=summany_average_row_index, column=summany_data_column_index-2).value = round(early_miles_lapsed/early_total, 2) if early_total > 0 else 0
                summany_average_row_index += 1
                claim_sheet.cell(row=summany_average_row_index, column=summany_data_column_index-4).value = "Time Lapsed"
                claim_sheet.cell(row=summany_average_row_index, column=summany_data_column_index-2).value = round(early_time_lapsed/early_total, 2) if early_total > 0 else 0
                summany_average_row_index += 1
            
            # auto adjust code
            for col in claim_sheet.columns:
                max_length = 0
                try:
                    column = col[0].column_letter # Get the column name
                    if column == 'I':
                        continue
                except:
                    continue
                for cell in col:
                    if cell.coordinate in claim_sheet.merged_cells: # not check merge_cells
                        continue
                    try: # Necessary to avoid error on empty cells
                        if len(str(cell.value)) > max_length:
                            max_length = len(cell.value)
                    except:
                        pass
                adjusted_width = (max_length + 2) * 1.2
                claim_sheet.column_dimensions[column].width = adjusted_width
    
    buff = BytesIO()
    workbook.save(buff)
    file = InMemoryUploadedFile(buff, "xlsx", f"{reportObj.id}.xlsx", None, buff.tell(), None)
    reportObj.file.save(f"{user.name}-{reportObj.id}-claim_reports.xlsx", file)
    reportObj.status = ProgressStatus.SUCCESS
    reportObj.save()