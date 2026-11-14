// Original educational example for the public firmware engineering guide.
// Matches the BAR implementation port contract in the pinned upstream project.
`timescale 1ns/1ps
module guide_bar (
    input logic rst,
    input logic clk,
    input logic [31:0] wr_addr,
    input logic [3:0] wr_be,
    input logic [31:0] wr_data,
    input logic wr_valid,
    input logic [87:0] rd_req_ctx,
    input logic [31:0] rd_req_addr,
    input logic rd_req_valid,
    output logic [87:0] rd_rsp_ctx,
    output logic [31:0] rd_rsp_data,
    output logic rd_rsp_valid
);
    localparam logic [31:0] MAGIC = 32'h47554944;
    localparam logic [31:0] BUILD = 32'h00020001;
    logic [31:0] scratch, cycles;
    logic [31:0] data_stage;
    logic [87:0] ctx_stage;
    logic valid_stage;
    integer lane;

    always_ff @(posedge clk) begin
        if (rst) begin
            scratch <= 0;
            cycles <= 0;
            data_stage <= 0;
            ctx_stage <= 0;
            valid_stage <= 0;
            rd_rsp_ctx <= 0;
            rd_rsp_data <= 0;
            rd_rsp_valid <= 0;
        end else begin
            cycles <= cycles + 1;
            // One owner; byte enables update only the selected lanes.
            if (wr_valid && wr_addr[11:0] == 12'h008) begin
                for (lane = 0; lane < 4; lane = lane + 1)
                    if (wr_be[lane])
                        scratch[lane*8 +: 8] <= wr_data[lane*8 +: 8];
            end
            // Snapshot data and carry the opaque context through the pipeline.
            valid_stage <= rd_req_valid;
            ctx_stage <= rd_req_ctx;
            case (rd_req_addr[11:0])
                12'h000: data_stage <= MAGIC;
                12'h004: data_stage <= BUILD;
                12'h008: data_stage <= scratch;
                12'h00c: data_stage <= cycles;
                default: data_stage <= 0;
            endcase
            rd_rsp_valid <= valid_stage;
            rd_rsp_ctx <= ctx_stage;
            rd_rsp_data <= data_stage;
        end
    end
endmodule
